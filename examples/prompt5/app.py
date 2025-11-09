import viktor as vkt
import requests

AEC_GRAPHQL_URL = "https://developer.api.autodesk.com/aec/graphql"

def execute_graphql(query: str, token: str, region: str, variables: dict | None = None, timeout: int = 30):
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
    return body["data"]

Q_WALLS_TYPES_MATERIALS = """
query WallsTypesMaterials($elementGroupId: ID!, $rsql: String!, $pagination: PaginationInput) {
  elementsByElementGroup(
    elementGroupId: $elementGroupId,
    filter: { query: $rsql },
    pagination: $pagination
  ) {
    pagination { cursor pageSize }
    results {
      id
      name
      references(filter: { names: ["Type"] }) {
        results {
          value {
            id
            name
            references(filter: { names: ["Structural Material", "Material"] }) {
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

class Parametrization(vkt.Parametrization):
    autodesk_file = vkt.AutodeskFileField(
        "Select a file",
        oauth2_integration="aps-integration-viktor",
    )

class Controller(vkt.Controller):
    parametrization = Parametrization

    @vkt.TableView("Walls, Type, Material")
    def table_view(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        region = params.autodesk_file.get_region(token)
        element_group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        rsql = "property.name.category==Walls and 'property.name.Element Context'==Instance"

        rows = []
        row_headers = []
        cursor = None

        while True:
            pagination = {"limit": 500}
            if cursor:
                pagination["cursor"] = cursor

            data = execute_graphql(
                Q_WALLS_TYPES_MATERIALS,
                token,
                region,
                variables={
                    "elementGroupId": element_group_id,
                    "rsql": rsql,
                    "pagination": pagination,
                },
            )

            block = data.get("elementsByElementGroup") or {}
            for el in block.get("results", []):
                el_id = el.get("id") or ""
                el_name = el.get("name") or ""

                type_name = ""
                material_name = ""

                refs = (el.get("references") or {}).get("results") or []
                if refs:
                    type_value = (refs[0] or {}).get("value") or {}
                    type_name = type_value.get("name") or ""

                    type_refs = (type_value.get("references") or {}).get("results") or []
                    # prefer Structural Material, then Material
                    mat = next((r for r in type_refs if r.get("name") == "Structural Material" and r.get("displayValue")), None)
                    if not mat:
                        mat = next((r for r in type_refs if r.get("name") == "Material" and r.get("displayValue")), None)
                    material_name = (mat or {}).get("displayValue") or ""

                rows.append([el_id, el_name, type_name, material_name])
                row_headers.append(f"Wall {len(row_headers) + 1}")

            cursor = (block.get("pagination") or {}).get("cursor")
            if not cursor:
                break

        return vkt.TableResult(
            rows,
            row_headers=row_headers,
            column_headers=["Element Id", "Element Name", "Type", "Material"],
        )
