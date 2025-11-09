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

    @vkt.TableView("Structural Framing Paint Cost Analysis")
    def table_view(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        # Get region and AEC Data Model group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # GraphQL query to get Structural Framing instances with Paint Area
        query = """
        query StructuralFramingPaintArea($elementGroupId: ID!) {
          elementsByElementGroup(
            elementGroupId: $elementGroupId, 
            filter: { query: "property.name.category=='Structural Framing' and 'property.name.Element Context'==Instance" }
          ) {
            results {
              name
              properties(filter: { names: ["Paint Area"] }) {
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
        paint_cost_per_sqm = 7.0  # $7 per m²

        elements = data.get("elementsByElementGroup", {}).get("results", [])
        
        for i, element in enumerate(elements, 1):
            element_name = element.get("name", f"Element {i}")
            paint_area = None
            paint_area_value = 0.0
            unit = ""
            
            # Extract Paint Area property
            properties = element.get("properties", {}).get("results", [])
            for prop in properties:
                if prop.get("name") == "Paint Area":
                    paint_area_value = float(prop.get("value", 0))
                    unit = prop.get("definition", {}).get("units", {}).get("name", "")
                    paint_area = f"{paint_area_value} {unit}"
                    break
            
            if paint_area is None:
                paint_area = "N/A"
                paint_cost = "N/A"
            else:
                # Calculate paint cost (assuming area is in m²)
                # If unit is different, you might need conversion logic here
                paint_cost = f"${paint_area_value * paint_cost_per_sqm:.2f}"
            
            table_data.append([element_name, paint_area, paint_cost])
            row_headers.append(f"Framing {i}")

        # Handle case when no elements are found
        if not table_data:
            table_data = [["No structural framing elements found", "N/A", "N/A"]]
            row_headers = ["No Data"]

        return vkt.TableResult(
            table_data,
            row_headers=row_headers,
            column_headers=["Element Name", "Paint Area", "Paint Cost ($7/m²)"],
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
