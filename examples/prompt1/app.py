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

    @vkt.TableView("Structural Framing Lengths")
    def table_view(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        # Get region and AEC Data Model group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # Query to get structural framing instances with their lengths
        query = """
        query StructuralFramingLengths($elementGroupId: ID!) {
          elementsByElementGroup(
            elementGroupId: $elementGroupId, 
            filter: { query: "property.name.category=='Structural Framing' and 'property.name.Element Context'==Instance" }
          ) {
            results {
              name
              properties(filter: { names: ["Family Name", "Length", "Cut Length"] }) {
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
        elements = data.get("elementsByElementGroup", {}).get("results", [])
        
        table_data = []
        row_headers = []
        
        for idx, element in enumerate(elements, 1):
            element_name = element.get("name", "Unknown")
            family_name = "Unknown"
            length_value = "N/A"
            length_unit = ""
            cut_length_value = "N/A"
            cut_length_unit = ""
            
            # Extract properties
            properties = element.get("properties", {}).get("results", [])
            for prop in properties:
                prop_name = prop.get("name")
                if prop_name == "Family Name":
                    family_name = prop.get("value", "Unknown")
                elif prop_name == "Length":
                    length_value = prop.get("value", "N/A")
                    units = prop.get("definition", {}).get("units")
                    if units:
                        length_unit = units.get("name", "")
                elif prop_name == "Cut Length":
                    cut_length_value = prop.get("value", "N/A")
                    units = prop.get("definition", {}).get("units")
                    if units:
                        cut_length_unit = units.get("name", "")
            
            # Use Cut Length if available, otherwise fallback to Length
            if cut_length_value != "N/A":
                final_length = cut_length_value
                final_unit = cut_length_unit
            else:
                final_length = length_value
                final_unit = length_unit
            
            # Format final length with unit
            if final_unit:
                length_display = f"{final_length} {final_unit}"
            else:
                length_display = str(final_length)
            
            table_data.append([element_name, family_name, length_display])
            row_headers.append(f"Element {idx}")

        return vkt.TableResult(
            table_data,
            row_headers=row_headers,
            column_headers=["Element Name", "Family Name", "Length"],
        )
