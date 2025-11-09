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
    min_diameter = vkt.NumberField(
        "Minimum Diameter (mm)",
        default=100,
        min=0,
    )


class Controller(vkt.Controller):
    parametrization = Parametrization

    @vkt.TableView("Pipes by Diameter")
    def table_view(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        # Get region and AEC Data Model group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # Query to get pipe elements with diameter greater than min_diameter
        rsql_filter = f"property.name.category==Pipes and 'property.name.Element Context'==Instance and property.name.Diameter>{params.min_diameter}"
        
        query = """
        query PipesByDiameter($elementGroupId: ID!, $rsqlFilter: String!) {
          elementsByElementGroup(
            elementGroupId: $elementGroupId,
            filter: { query: $rsqlFilter }
          ) {
            results {
              id
              name
              properties(filter: { names: ["Diameter", "Length", "Family Name"] }) {
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

        variables = {
            "elementGroupId": group_id,
            "rsqlFilter": rsql_filter
        }

        # Execute the GraphQL query
        data = execute_graphql(query, token, region, variables)

        # Post-processing of data
        results = data.get("elementsByElementGroup", {}).get("results", [])
        
        if not results:
            raise vkt.UserError(f"No pipes found with diameter greater than {params.min_diameter} mm")

        table_data = []
        row_headers = []
        
        for idx, element in enumerate(results, 1):
            element_name = element.get("name", "Unknown")
            element_id = element.get("id", "")
            
            # Extract properties
            props = element.get("properties", {}).get("results", [])
            diameter = ""
            length = ""
            family_name = ""
            
            for prop in props:
                prop_name = prop.get("name", "")
                prop_value = prop.get("value", "")
                
                # Safely extract units
                definition = prop.get("definition")
                unit = ""
                if definition:
                    units = definition.get("units")
                    if units:
                        unit = units.get("name", "")
                
                if prop_name == "Diameter":
                    diameter = f"{prop_value} {unit}" if unit else str(prop_value)
                elif prop_name == "Length":
                    length = f"{prop_value} {unit}" if unit else str(prop_value)
                elif prop_name == "Family Name":
                    family_name = str(prop_value)
            
            table_data.append([element_id, element_name, family_name, diameter, length])
            row_headers.append(f"Pipe {idx}")

        return vkt.TableResult(
            table_data,
            row_headers=row_headers,
            column_headers=["Element ID", "Name", "Family Name", "Diameter", "Length"],
        )
