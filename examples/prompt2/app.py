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

    @vkt.AutodeskView("3D Model")
    def autodesk_view(self, params, **kwargs):
        """Display the 3D model from the selected Autodesk file."""
        if not params.autodesk_file:
            raise vkt.UserError("Please select an Autodesk file")
        
        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()
        
        return vkt.AutodeskResult(params.autodesk_file, access_token=token)

    @vkt.TableView("Doors (900mm < Width < 1200mm)")
    def table_view(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        # Get region and AEC Data Model group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # GraphQL query to get Door instances with Width between 900mm and 1200mm
        query = """
        query FilteredDoors($elementGroupId: ID!) {
          elementsByElementGroup(
            elementGroupId: $elementGroupId, 
            filter: { query: "property.name.category==Doors and property.name.Width>900 and property.name.Width<1200 and 'property.name.Element Context'==Instance" }
          ) {
            results {
              name
              properties(filter: { names: ["Family Name", "Width", "Height"] }) {
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

        variables = {"elementGroupId": group_id}

        # Execute the GraphQL query
        data = execute_graphql(query, token, region, variables)

        # Post-processing of data
        table_data = []
        row_headers = []

        elements = data.get("elementsByElementGroup", {}).get("results", [])
        
        for i, element in enumerate(elements, 1):
            element_name = element.get("name", f"Element {i}")
            family_name = "N/A"
            width = "N/A"
            height = "N/A"
            
            # Extract properties
            properties = element.get("properties", {}).get("results", [])
            for prop in properties:
                prop_name = prop.get("name")
                prop_value = prop.get("value", "")
                
                # Safely extract unit information
                definition = prop.get("definition")
                unit = ""
                if definition:
                    units = definition.get("units")
                    if units:
                        unit = units.get("name", "")
                
                if prop_name == "Family Name":
                    family_name = prop_value
                elif prop_name == "Width":
                    width = f"{prop_value} {unit}" if unit else prop_value
                elif prop_name == "Height":
                    height = f"{prop_value} {unit}" if unit else prop_value
            
            table_data.append([element_name, family_name, width, height])
            row_headers.append(f"Door {i}")

        # Handle case when no elements are found
        if not table_data:
            table_data = [["No doors found matching criteria", "N/A", "N/A", "N/A"]]
            row_headers = ["No Data"]

        return vkt.TableResult(
            table_data,
            row_headers=row_headers,
            column_headers=["Element Name", "Family Name", "Width", "Height"],
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
