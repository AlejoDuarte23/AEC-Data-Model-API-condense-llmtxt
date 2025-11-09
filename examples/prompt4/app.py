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

    @vkt.TableView("Model Categories", duration_guess=10)
    def categories_table(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        # Get region and AEC Data Model group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # Query to get distinct category values with their counts
        query = """
        query UsedCategories($elementGroupId: ID!, $limit: Int!) {
          distinctPropertyValuesInElementGroupByName(
            elementGroupId: $elementGroupId
            name: "Category"
            filter: { query: "'property.name.Element Context'==Instance" }
          ) {
            results {
              values(limit: $limit) {
                value
                count
              }
            }
          }
        }
        """

        variables = {"elementGroupId": group_id, "limit": 1000}

        # Execute the GraphQL query
        data = execute_graphql(query, token, region, variables)

        # Parse results
        block = data.get("distinctPropertyValuesInElementGroupByName") or {}
        results_list = block.get("results") or []

        values = []
        for r in results_list:
            values.extend(r.get("values") or [])

        # Build table data
        table_data = []
        row_headers = []
        for idx, item in enumerate(values, 1):
            category = item.get("value", "Unknown")
            count = item.get("count", 0)
            table_data.append([category, count])
            row_headers.append(f"Category {idx}")

        return vkt.TableResult(
            table_data,
            row_headers=row_headers,
            column_headers=["Category Name", "Instance Count"],
        )

    @vkt.TableView("Model Families", duration_guess=10)
    def families_table(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        # Get region and AEC Data Model group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # Query to get distinct family names with their counts
        query = """
        query UsedFamilyNames($elementGroupId: ID!, $limit: Int!) {
          distinctPropertyValuesInElementGroupByName(
            elementGroupId: $elementGroupId
            name: "Family Name"
            filter: { query: "'property.name.Element Context'==Instance" }
          ) {
            results {
              values(limit: $limit) {
                value
                count
              }
            }
          }
        }
        """

        variables = {"elementGroupId": group_id, "limit": 1000}

        # Execute the GraphQL query
        data = execute_graphql(query, token, region, variables)

        # Parse results
        block = data.get("distinctPropertyValuesInElementGroupByName") or {}
        results_list = block.get("results") or []

        values = []
        for r in results_list:
            values.extend(r.get("values") or [])

        # Build table data
        table_data = []
        row_headers = []
        for idx, item in enumerate(values, 1):
            family = item.get("value", "Unknown")
            count = item.get("count", 0)
            table_data.append([family, count])
            row_headers.append(f"Family {idx}")

        return vkt.TableResult(
            table_data,
            row_headers=row_headers,
            column_headers=["Family Name", "Instance Count"],
        )

    @vkt.TableView("Wall Areas", duration_guess=15)
    def walls_area_table(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        # Get region and AEC Data Model group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # Query to get wall instances with their areas
        query = """
        query WallAreasRSQL($elementGroupId: ID!) {
          elementsByElementGroup(
            elementGroupId: $elementGroupId, 
            filter: { query: "property.name.category==Walls and 'property.name.Element Context'==Instance" }
          ) {
            results {
              id
              name
              properties(filter: { names: ["Area"] }) {
                results {
                  name
                  value
                  definition { 
                    units { 
                      name 
                    } 
                  }
                }
              }
            }
          }
        }
        """

        variables = {"elementGroupId": group_id}

        # Execute the GraphQL query
        data = execute_graphql(query, token, region, variables)

        # Parse results
        elements = data.get("elementsByElementGroup", {}).get("results", [])

        # Build table data
        table_data = []
        row_headers = []
        total_area = 0.0
        unit = ""

        for idx, element in enumerate(elements, 1):
            element_id = element.get("id", "")
            element_name = element.get("name", "Unnamed")
            
            # Get area property
            properties = element.get("properties", {}).get("results", [])
            area_value = 0.0
            
            for prop in properties:
                if prop.get("name") == "Area":
                    try:
                        area_value = float(prop.get("value", 0))
                    except (ValueError, TypeError):
                        area_value = 0.0
                    
                    # Get unit (safely)
                    if not unit:
                        definition = prop.get("definition")
                        if definition:
                            units = definition.get("units")
                            if units:
                                unit = units.get("name", "")
            
            total_area += area_value
            table_data.append([element_name, area_value, unit or ""])
            row_headers.append(f"Wall {idx}")

        # Add total row
        table_data.append(["TOTAL", total_area, unit or ""])
        row_headers.append("Total")

        return vkt.TableResult(
            table_data,
            row_headers=row_headers,
            column_headers=["Wall Name", "Area", "Unit"],
        )
