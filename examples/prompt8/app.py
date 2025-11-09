import viktor as vkt
import requests

AEC_GRAPHQL_URL = "https://developer.api.autodesk.com/aec/graphql"

def execute_graphql(query: str, token: str, region: str, variables: dict = None, timeout: int = 30):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Region": region,
    }
    payload = {"query": query, "variables": variables or {}}
    resp = requests.post(AEC_GRAPHQL_URL, headers=headers, json=payload, timeout=timeout)
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code}: {resp.text}")
    body = resp.json()
    if body.get("errors"):
        raise RuntimeError(f"GraphQL errors: {body['errors']}")
    return body.get("data", {})


class Parametrization(vkt.Parametrization):
    autodesk_file = vkt.AutodeskFileField(
        "Select a file",
        oauth2_integration="aps-integration-viktor",
    )


class Controller(vkt.Controller):
    parametrization = Parametrization

    @vkt.TableView("Walls by Structural Material")
    def table_view(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        # Get region and AEC Data Model group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # Query to get wall instances with their area and structural material from type
        query = """
        query WallsByMaterial($elementGroupId: ID!, $pagination: PaginationInput) {
          elementsByElementGroup(
            elementGroupId: $elementGroupId,
            filter: { query: "property.name.category==Walls and 'property.name.Element Context'==Instance" },
            pagination: $pagination
          ) {
            pagination { cursor pageSize }
            results {
              id
              name
              properties(filter: { names: ["Area"] }) {
                results {
                  name
                  value
                  definition { units { name } }
                }
              }
              references(filter: { names: ["Type"] }) {
                results {
                  value {
                    id
                    name
                    references(filter: { names: ["Structural Material"] }) {
                      results {
                        name
                        displayValue
                        value { id }
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """

        # Fetch all walls with pagination
        all_walls = []
        cursor = None
        limit = 100

        while True:
            variables = {
                "elementGroupId": group_id,
                "pagination": {"limit": limit} if not cursor else {"cursor": cursor, "limit": limit},
            }
            data = execute_graphql(query, token, region, variables)
            block = data.get("elementsByElementGroup", {}) or {}
            page_results = block.get("results", []) or []
            all_walls.extend(page_results)

            page = block.get("pagination", {}) or {}
            new_cursor = page.get("cursor")

            if not new_cursor or new_cursor == cursor or len(page_results) == 0:
                break
            cursor = new_cursor

        # Process walls and group by structural material
        material_data = {}

        for wall in all_walls:
            # Extract area
            area = None
            props = (wall.get("properties") or {}).get("results") or []
            for prop in props:
                if prop.get("name") == "Area":
                    area = prop.get("value")
                    break

            if area is None:
                continue

            # Extract structural material from type reference
            material_name = "Unknown"
            refs = (wall.get("references") or {}).get("results") or []
            if refs:
                type_value = (refs[0] or {}).get("value") or {}
                type_refs = (type_value.get("references") or {}).get("results") or []
                mat = next((r for r in type_refs if r.get("name") == "Structural Material" and r.get("displayValue")), None)
                if mat:
                    material_name = mat.get("displayValue") or "Unknown"

            # Group by material
            if material_name not in material_data:
                material_data[material_name] = {
                    "count": 0,
                    "total_area": 0.0,
                    "areas": []
                }

            material_data[material_name]["count"] += 1
            material_data[material_name]["total_area"] += area
            material_data[material_name]["areas"].append(area)

        # Filter materials with more than 3 walls
        filtered_materials = {
            mat: data for mat, data in material_data.items() if data["count"] > 3
        }

        if not filtered_materials:
            raise vkt.UserError("No materials found with more than 3 walls")

        # Prepare table data
        table_data = []
        row_headers = []

        for material, data in sorted(filtered_materials.items()):
            count = data["count"]
            total_area = data["total_area"]
            avg_area = total_area / count if count > 0 else 0

            table_data.append([
                material,
                count,
                round(total_area, 2),
                round(avg_area, 2)
            ])
            row_headers.append(f"Material {len(row_headers) + 1}")

        column_headers = ["Structural Material", "Number of Walls", "Total Area", "Average Area"]

        return vkt.TableResult(
            table_data,
            row_headers=row_headers,
            column_headers=column_headers,
        )
