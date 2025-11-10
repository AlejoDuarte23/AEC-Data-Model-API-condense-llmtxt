# AEC Data Model LLm.txt

## 1. Making GraphQL Requests

```python
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

    @vkt.TableView("Model Categories")
    def table_view(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("aps-integration-viktor")
        token = integration.get_access_token()

        # Get region and AEC Data Model group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # Query to get distinct category values with their counts
        query = """ """

        variables = {"elementGroupId": group_id, ...}

        # Execute the GraphQL query
        data = execute_graphql(query, token, region, variables)

        # Post-processing of data
        table_data = ...
        # Generate row headers


        return vkt.TableResult(
            filtered_categories,
            row_headers=...,
            column_headers=...,
        )
```

## 2. elementsByElementGroup

### 2.1. Get the total length of each instance of Structural Framings

```graphql
query StructuralFramingLengthsRSQL($elementGroupId: ID!) {
  elementsByElementGroup(
    elementGroupId: $elementGroupId, 
    filter: { query: "property.name.category=='Structural Framing' and 'property.name.Element Context'==Instance" }
  ) {
    results {
      name
      properties(filter: { names: ["Length", "Cut Length"] }) {
        results {
          name
          value
          definition { units { name } }
        }
      }
    }
  }
}
```


### 2.2. Get the area of each Wall element

**RSQL Filtering:** Use a query string:
```plaintext
filter: { query: "property.name.category==Walls and 'property.name.Element Context'==Instance" }
```

and request the Area property similarly. In a full query form:

```graphql
query WallAreasRSQL($id: ID!) {
  elementsByElementGroup(elementGroupId: $id, filter: { query: "property.name.category==Walls and 'property.name.Element Context'==Instance" }) {
    results {
      name
      properties(filter: { names: ["Area"] }) {
        results { name, value, definition { units { name } } }
      }
    }
  }
}
```



### 2.3. Get the weight of Structural Framings

**RSQL Filtering:**

```graphql
query FramingWeightsRSQL($id: ID!) {
  elementsByElementGroup(elementGroupId: $id, filter: { query: "property.name.category=='Structural Framing' and 'property.name.Element Context'==Instance" }) {
    results {
      name
      properties(filter: { names: ["Weight"] }) {
        results { name, value, definition { units { name } } }
      }
    }
  }
}
```

- The filter string is the same as the length query (select all structural framing instances), and we retrieve Weight.



### 2.4. Filter Doors

**RSQL Approach:**
```graphql
query NarrowDoorsRSQL($id: ID!) {
  elementsByElementGroup(elementGroupId: $id, filter: { query: "property.name.category==Doors and property.name.Width<700 and 'property.name.Element Context'==Instance" }) {
    results {
      id
      name
      properties(filter: { names: ["Width"] }) {
        results { name, value }
      }
    }
  }
}
```

- Filter string: `category==Doors and Width<700 and Element Context==Instance`. This yields the same set. The results would list doors maybe with their width values (you could include more door info if needed, like door name or family, but here just demonstrating width).

## 3. Get specific properties from the types [Important]

Most measurable values are **instance properties**, because they depend on placement, orientation, and extents. Examples include Area, Volume, Length, Cut Length, Width, Height, Level, Phase. Shared definitions are **type properties**. Examples include Family Name, Type Name, Type Mark, Function, Thickness, Structural Material.

### 3.1. Get materials from element Types using references

```graphql
query WallsTypesMaterialsPaginated($elementGroupId: ID!, $pagination: PaginationInput) {
  elementsByElementGroup(
    elementGroupId: $elementGroupId,
    filter: { query: "property.name.category==Walls and 'property.name.Element Context'==Instance" },
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
```

- This retrieves Wall instances and navigates to their Type reference, then accesses the material references (`Structural Material`) from the Type. Use `displayValue` to get the formatted material name.

**Python snippet to extract Structural Material:**
```python
# Extract structural material from type reference
material_name = ""
refs = (wall.get("references") or {}).get("results") or []
if refs:
    type_value = (refs[0] or {}).get("value") or {}
    type_refs = (type_value.get("references") or {}).get("results") or []
    # look for Structural Material reference
    mat = next((r for r in type_refs if r.get("name") == "Structural Material" and r.get("displayValue")), None)
    material_name = (mat or {}).get("displayValue") or ""

if not material_name:
    material_name = "Unknown"
```

## 4. distinctPropertyValuesInElementGroupByName

"Distinct values" queries save you from doing your own deduplication. The trick is simple: use the **filter** to choose the population you care about, then ask the API to return unique values for a single property, with a server-side count.

**Important:** This query doesn't support pagination. Parse results as follows:
```python
data = execute_graphql(query, token, region, variables)
block = data.get("distinctPropertyValuesInElementGroupByName") or {}
results_list = block.get("results") or []

values = []
for r in results_list:
    values.extend(r.get("values") or [])
```

### 4.1. Categories that are used in the model
Only categories with at least one placed element. Filter on **Instance**.
```graphql
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
```

### 4.2. All family names from category X -> Walls example
All families defined in the "Walls" category.

```graphql
query FamilyNamesInCategory($elementGroupId: ID!, $limit: Int) {
  distinctPropertyValuesInElementGroupByName(
    elementGroupId: $elementGroupId
    name: "Family Name"
    filter: { query: "property.name.category==Walls and 'property.name.Element Context'==Instance" }
  ) {
    results {
      values(limit: $limit) {
        value
        count
      }
    }
  }
}
```
`count` here is the number of instances with that family name inside the category, not type definitions.

### 4.3. Family names that are used in the model
Preferred path, if "Family Name" is available on instances in your model build: filter on **Instance**.
```graphql
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
```


## 5. Pagination

- Send `pagination.limit` in the request, never `pageSize`.
- The response returns `pagination.cursor` and `pagination.pageSize`.
- Start with `limit` only, then keep calling with the returned cursor.
- Treat the cursor as opaque; do not modify it.
- Stop when the cursor is empty, or when the service repeats the same cursor, or when a page has zero results.

```graphql
query Example($elementGroupId: ID!, $pagination: PaginationInput) {
  elementsByElementGroup(
    elementGroupId: $elementGroupId,
    filter: { query: "'property.name.Element Context'==Instance" },
    pagination: $pagination
  ) {
    pagination { cursor pageSize }
    results { id name }
  }
}
```

### 5.1. Python while loop

```python
import requests

AEC_GRAPHQL_URL = "https://developer.api.autodesk.com/aec/graphql"

def execute_graphql(query: str, token: str, region: str, variables: dict = None, timeout: int = 30) -> dict:
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

QUERY = """
query Example($elementGroupId: ID!, $pagination: PaginationInput) {
  elementsByElementGroup(
    elementGroupId: $elementGroupId,
    filter: { query: "'property.name.Element Context'==Instance" },
    pagination: $pagination
  ) {
    pagination { cursor pageSize }
    results { id name }
  }
}
"""

def fetch_all_elements(element_group_id: str, token: str, region: str, limit: int = 100) -> list[dict]:
    all_results = []
    cursor = None
    while True:
        variables = {
            "elementGroupId": element_group_id,
            "pagination": {"limit": limit} if not cursor else {"cursor": cursor, "limit": limit},
        }
        data = execute_graphql(QUERY, token, region, variables)
        block = data.get("elementsByElementGroup", {}) or {}
        page_results = block.get("results", []) or []
        all_results.extend(page_results)

        page = block.get("pagination", {}) or {}
        new_cursor = page.get("cursor")

        # stop on empty cursor, on repeated cursor, or on empty page
        if not new_cursor or new_cursor == cursor or len(page_results) == 0:
            break
        cursor = new_cursor

    return all_results
```

## 6. RSQL Query Syntax - Quoting Rules

When writing RSQL filter queries, proper quoting is essential to avoid parsing errors:

**CRITICAL: RSQL filters do NOT support GraphQL variable interpolation.** You cannot use `$variable` inside the RSQL filter string. Instead, construct the filter string with actual values in Python, then pass it as a GraphQL variable:

```python
# ❌ WRONG - This will NOT work:
query = """
query Example($elementGroupId: ID!, $minValue: Float!) {
  elementsByElementGroup(
    elementGroupId: $elementGroupId,
    filter: { query: "property.name.Width>$minValue" }  # GraphQL variable in RSQL - ERROR!
  ) { ... }
}
"""

# ✅ CORRECT - Construct the RSQL filter string first:
rsql_filter = f"property.name.Width>{params.min_value}"
query = """
query Example($elementGroupId: ID!, $rsqlFilter: String!) {
  elementsByElementGroup(
    elementGroupId: $elementGroupId,
    filter: { query: $rsqlFilter }  # Pass the entire filter string as a variable
  ) { ... }
}
"""
variables = {"elementGroupId": group_id, "rsqlFilter": rsql_filter}
```

**Rules for quoting:**
1. **Property names with spaces** must be enclosed in single quotes: `'property.name.Element Context'`
2. **Property values with spaces** must be enclosed in single quotes: `'Structural Framing'`, `'Cut Length'`
3. **Property names without spaces** don't require quotes: `property.name.category`, `property.name.Width`
4. **Property values without spaces** don't require quotes: `category==Walls`, `Width<700`
5. **For `=contains=` operator**: Neither property names nor values need quotes, even with spaces: `property.name.Material=contains=Concrete`

**Examples:**
- ✅ Correct: `property.name.category=='Structural Framing'`
- ❌ Wrong: `property.name.category==Structural Framing` (will cause parsing error)
- ✅ Correct: `'property.name.Element Context'==Instance`
- ❌ Wrong: `property.name.Element Context==Instance` (will cause parsing error)
- ✅ Correct: `property.name.category==Walls and property.name.Width<700`
- ✅ Correct: `'property.name.Cut Length'>1000` (property name with space)
- ✅ Correct: `property.name.Material=contains=Concrete` (contains operator)
- ❌ Wrong: `'property.name.Material'=contains="Concrete"` (don't quote with contains)

**Complete filter examples:**
```
filter: { query: "property.name.category=='Structural Framing' and 'property.name.Element Context'==Instance" }
filter: { query: "property.name.Material=contains=Concrete" }
```

## 7. Notes

### 7.1. Category is NOT a Property
**Important:** `Category` is not a queryable property in the AEC Data Model. It's a metadata field used in RSQL filters but cannot be retrieved as a property. To identify element types in your results:
- Use **`Family Name`** (instance or type property) - identifies the family of the element
- Use **`Type Name`** (type property) - identifies the specific type within a family
- Use the RSQL filter `property.name.category==<CategoryName>` to filter by category, but retrieve Family Name or Type Name to display the element classification

**Example of correct approach:**
```python
# Filter by category in RSQL, but retrieve Family Name
query = """
query Elements($elementGroupId: ID!) {
  elementsByElementGroup(
    elementGroupId: $elementGroupId,
    filter: { query: "property.name.category==Walls and 'property.name.Element Context'==Instance" }
  ) {
    results {
      name
      properties(filter: { names: ["Family Name", "Type Name"] }) {
        results { name, value }
      }
    }
  }
}
"""
```

### 7.2. Property Units Can Be None
When accessing property units from GraphQL responses, the `units` field can be `None` for certain properties (e.g., "Family Name" or other non-dimensional properties). Always check if `definition`, `units`, and `name` exist before accessing them to avoid `AttributeError`.

**Example of safe unit extraction:**
```python
definition = prop.get("definition")
unit = ""
if definition:
    units = definition.get("units")
    if units:
        unit = units.get("name", "")
```

## 8. Get ElementGroupId 
To make querys get the elementgroupId from `vkt.AutodeskFileField` using `get_aec_data_model_element_group_id`

```python
import viktor as vkt
import requests

AEC_GRAPHQL_URL = "https://developer.api.autodesk.com/aec/graphql"

def execute_graphql(query: str, token: str, region: str, variables: dict = None, timeout: int = 30):
  ...


class Parametrization(vkt.Parametrization):
    autodesk_file = vkt.AutodeskFileField(
        "Select a file",
        oauth2_integration="user-aps-integration",
    )

class Controller(vkt.Controller):
    parametrization = Parametrization

    def autodesk_work(self, params, **kwargs):
        if not params.autodesk_file:
            raise vkt.UserError("Select a file in the Autodesk field")

        # Initialize the integration and get an access token
        integration = vkt.external.OAuth2Integration("user-aps-integration")
        token = integration.get_access_token()

        # Get region and AEC Data Model element group ID from Autodesk file
        region = params.autodesk_file.get_region(token)
        group_id = params.autodesk_file.get_aec_data_model_element_group_id(token)

        # (query elements, retrieve model metadata, etc.
```