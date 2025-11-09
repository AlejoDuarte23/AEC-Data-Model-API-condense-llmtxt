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

    @vkt.TableView("Walls and Floors - Material & Volume")
    def walls_floors_table(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        # Get region and AEC Data Model group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # Query for Walls and Floors with Structural Material and Volume
        query = """
        query WallsFloorsData($elementGroupId: ID!, $pagination: PaginationInput) {
          elementsByElementGroup(
            elementGroupId: $elementGroupId,
            filter: { query: "(property.name.category==Walls or property.name.category==Floors) and 'property.name.Element Context'==Instance" },
            pagination: $pagination
          ) {
            pagination { cursor pageSize }
            results {
              id
              name
              properties(filter: { names: ["Volume"] }) {
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
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """

        # Fetch all elements with pagination
        all_results = []
        cursor = None
        while True:
            variables = {
                "elementGroupId": group_id,
                "pagination": {"limit": 100} if not cursor else {"cursor": cursor, "limit": 100},
            }
            data = execute_graphql(query, token, region, variables)
            block = data.get("elementsByElementGroup", {}) or {}
            page_results = block.get("results", []) or []
            all_results.extend(page_results)

            page = block.get("pagination", {}) or {}
            new_cursor = page.get("cursor")

            if not new_cursor or new_cursor == cursor or len(page_results) == 0:
                break
            cursor = new_cursor

        # Process results
        table_data = []
        row_headers = []
        
        for elem in all_results:
            name = elem.get("name", "Unknown")
            
            # Get Volume
            volume = ""
            volume_unit = ""
            properties = elem.get("properties", {}).get("results", []) or []
            for prop in properties:
                if prop.get("name") == "Volume":
                    volume = prop.get("value", "")
                    definition = prop.get("definition")
                    if definition:
                        units = definition.get("units")
                        if units:
                            volume_unit = units.get("name", "")
            
            volume_str = f"{volume} {volume_unit}".strip() if volume else ""
            
            # Get Structural Material from Type reference
            material = ""
            references = elem.get("references", {}).get("results", []) or []
            for ref in references:
                ref_value = ref.get("value")
                if ref_value:
                    mat_refs = ref_value.get("references", {}).get("results", []) or []
                    for mat_ref in mat_refs:
                        if mat_ref.get("name") == "Structural Material":
                            material = mat_ref.get("displayValue", "")
                            break
                if material:
                    break
            
            table_data.append([material, volume_str])
            row_headers.append(name)

        return vkt.TableResult(
            table_data,
            row_headers=row_headers,
            column_headers=["Structural Material", "Volume"]
        )

    @vkt.TableView("Structural Columns & Framing - Paint, Weight")
    def structural_table(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        # Get region and AEC Data Model group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # Query for Structural Columns and Structural Framing
        query = """
        query StructuralData($elementGroupId: ID!, $pagination: PaginationInput) {
          elementsByElementGroup(
            elementGroupId: $elementGroupId,
            filter: { query: "(property.name.category=='Structural Columns' or property.name.category=='Structural Framing') and 'property.name.Element Context'==Instance" },
            pagination: $pagination
          ) {
            pagination { cursor pageSize }
            results {
              id
              name
              properties(filter: { names: ["Paint Area", "Weight", "Exact Weight"] }) {
                results {
                  name
                  value
                  definition { units { name } }
                }
              }
            }
          }
        }
        """

        # Fetch all elements with pagination
        all_results = []
        cursor = None
        while True:
            variables = {
                "elementGroupId": group_id,
                "pagination": {"limit": 100} if not cursor else {"cursor": cursor, "limit": 100},
            }
            data = execute_graphql(query, token, region, variables)
            block = data.get("elementsByElementGroup", {}) or {}
            page_results = block.get("results", []) or []
            all_results.extend(page_results)

            page = block.get("pagination", {}) or {}
            new_cursor = page.get("cursor")

            if not new_cursor or new_cursor == cursor or len(page_results) == 0:
                break
            cursor = new_cursor

        # Process results
        table_data = []
        row_headers = []
        
        for elem in all_results:
            name = elem.get("name", "Unknown")
            
            # Initialize property values
            paint_area = ""
            weight = ""
            exact_weight = ""
            
            properties = elem.get("properties", {}).get("results", []) or []
            for prop in properties:
                prop_name = prop.get("name")
                value = prop.get("value", "")
                unit = ""
                definition = prop.get("definition")
                if definition:
                    units = definition.get("units")
                    if units:
                        unit = units.get("name", "")
                
                value_str = f"{value} {unit}".strip() if value else ""
                
                if prop_name == "Paint Area":
                    paint_area = value_str
                elif prop_name == "Weight":
                    weight = value_str
                elif prop_name == "Exact Weight":
                    exact_weight = value_str
            
            table_data.append([paint_area, weight, exact_weight])
            row_headers.append(name)

        return vkt.TableResult(
            table_data,
            row_headers=row_headers,
            column_headers=["Paint Area", "Weight", "Exact Weight"]
        )

    def autodesk_work(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        # Get region and AEC Data Model group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # Do something with token, region, and group_id
        # (e.g., query elements, retrieve model metadata, etc.)
        # For now, just return a dictionary for inspection
        return {
            "region": region,
            "group_id": group_id,
        }
