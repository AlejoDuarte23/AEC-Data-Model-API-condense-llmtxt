
## Advance Filtering  

```
{ ..., "filter": { "query": "metadata.fileUrn=='urn:adsk.wipstg:dm.lineage:u-ncDS7gX3ZhpB3rgZXKeQ' or metadata.fileUrn=='urn:adsk.wipstg:dm.lineage:R8YVGN61QDaLElL0YSfkKg'" ... }
```

```
{ ..., "filter": { "query": "metadata.fileUrn=='urn:adsk.wipstg:dm.lineage:u-ncDS7gX3ZhpB3rgZXKeQ' and metadata.createdBy.email=='first.last@autodesk.com'" ... }
```

```
{ ..., "filter": { "query": "metadata.fileUrn=='urn:adsk.wipstg:dm.lineage:u-ncDS7gX3ZhpB3rgZXKeQ'" "createdBy": "first.last@autodesk.com" ... }
```

```
{ ..., "filter": { "query": "metadata.name=='Snowdon Towers East.rvt' and metadata.createdBy.email=='first.last@autodesk.com'" ... }
```

```
{ ..., "filter": { "query": "metadata.name=='Snowdon Towers East.rvt'", "createdBy": "first.last@autodesk.com" ... }
```

```
{ ..., "filter": { "query": "metadata.name=='Snowdon Towers East.rvt'", "name": "Snowdon Towers West.rvt" ... }
```

```
{ ..., "filter": { "query": "metadata.name=='Snowdon Towers East.rvt' or metadata.createdBy.email=='first.last@autodesk.com'" ... }
```

```
{ ..., "filter": { "query": "metadata.fileUrn=='urn:adsk.wipstg:dm.lineage:u-ncDS7gX3ZhpB3rgZXKeQ' or metadata.fileUrn=='urn:adsk.wipstg:dm.lineage:R8YVGN61QDaLElL0YSfkKg'" ... }
```

```
{ ..., "filter": { "query": "metadata.fileUrn=='urn:adsk.wipstg:dm.lineage:u-ncDS7gX3ZhpB3rgZXKeQ' and metadata.createdBy.email=='first.last@autodesk.com'" ... }
```

```
{ ..., "filter": { "query": "metadata.fileUrn=='urn:adsk.wipstg:dm.lineage:u-ncDS7gX3ZhpB3rgZXKeQ'" "createdBy": "first.last@autodesk.com" ... }
```

```
{ ..., "filter": { "query": "metadata.name=='Snowdon Towers East.rvt' and metadata.createdBy.email=='first.last@autodesk.com'" ... }
```

```
{ ..., "filter": { "query": "metadata.name=='Snowdon Towers East.rvt'", "createdBy": "first.last@autodesk.com" ... }
```

```
{ ..., "filter": { "query": "metadata.name=='Snowdon Towers East.rvt'", "name": "Snowdon Towers West.rvt" ... }
```

```
{ ..., "filter": { "query": "metadata.name=='Snowdon Towers East.rvt' or metadata.createdBy.email=='first.last@autodesk.com'" ... }
```


---
## STD Filtering 

```
{ ..., "filter": { "nameWithComparator": {"name": "Pipes", "comparator": "CONTAINS"} ... }
```

```
{ ..., "filter": { "name": "2.5\" x 5\" rectangular (Orange)" "properties": [ { "name": "Family Name", "value": "Rectangular Mullion" } { "id": "autodesk.revit.parameter:parameter.elementContext-1.0.0", "value": "Instance" } ] "references": { "name": "Type", "referencedId": "YWVjZX5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ351LW5jRFM3Z1E2R2hwQjNyZ1pYS2VRX2UzPLIz" } "createdBy": "first.last@autodesk.com" }, ... }
```

```
{ ..., "filter": { "fileUrn": ["urn:adsk.wipstg:dm.lineage:u-ncDS7gX3ZhpB3rgZXKeQ", "urn:adsk.wipstg:dm.lineage:R8YVGN61QDaLElL0YSfkKg"] ... }
```

```
{ ..., "filter": { "fileUrn": "urn:adsk.wipstg:dm.lineage:u-ncDS7gX3ZhpB3rgZXKeQ", "createdBy": "first.last@autodesk.com" ... }
```

```
{ ..., "filter": { "name": "Snowdon Towers East.rvt", "createdBy": "first.last@autodesk.com" ... }
```

```
{ ..., "filter": { "name": ["Snowdon Towers East.rvt", "Snowdon Towers West.rvt"] ... }
```

```
{ ..., "filter": { "nameWithComparator": {"name": "Pipes", "comparator": "CONTAINS"} ... }
```

```
{ ..., "filter": { "name": "2.5\" x 5\" rectangular (Orange)" "properties": [ { "name": "Family Name", "value": "Rectangular Mullion" } { "id": "autodesk.revit.parameter:parameter.elementContext-1.0.0", "value": "Instance" } ] "references": { "name": "Type", "referencedId": "YWVjZX5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ351LW5jRFM3Z1E2R2hwQjNyZ1pYS2VRX2UzPLIz" } "createdBy": "first.last@autodesk.com" }, ... }
```

```
{ ..., "filter": { "fileUrn": ["urn:adsk.wipstg:dm.lineage:u-ncDS7gX3ZhpB3rgZXKeQ", "urn:adsk.wipstg:dm.lineage:R8YVGN61QDaLElL0YSfkKg"] ... }
```

```
{ ..., "filter": { "fileUrn": "urn:adsk.wipstg:dm.lineage:u-ncDS7gX3ZhpB3rgZXKeQ", "createdBy": "first.last@autodesk.com" ... }
```

```
{ ..., "filter": { "name": "Snowdon Towers East.rvt", "createdBy": "first.last@autodesk.com" ... }
```

```
{ ..., "filter": { "name": ["Snowdon Towers East.rvt", "Snowdon Towers West.rvt"] ... }
```


## Request Elements matching the specified classification filter

```
query GetConcreteMaterials($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup( elementGroupId: $elementGroupId filter: {query: $propertyFilter} pagination: {limit: 20} ) { results { id name } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVB","propertyFilter":"property.name.category==Materials and 'property.name.Element Name'=contains='Concrete'"}
```

```
{"data":{"elementsByElementGroup":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzE1Nzc0Mw","name":"Concrete, Precast Smooth, Light Grey"},{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzFmYjFhNA","name":"Concrete, Polished"},{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzQ5ZmI","name":" ...etc
```

```
query GetInstancesOfConcreteMaterial($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup(elementGroupId: $elementGroupId, filter: { query: $propertyFilter}, pagination : { limit : 20 }) { results { id name properties { results { name value } } references{ results{ name displayValue value{ properties{ results{ name value displayValue } } } } } } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3","propertyFilter":"('reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJkNjE3 or 'reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJlZA) and 'property.name.Element Context'==Instance"}
```

```
{"data":{"elementsByElementGroup":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzkzZjc1","name":"CC24x24","properties":{"results":[{"name":"Comments","value":null},{"name":"Has Association","value":false},{"name":"Column Location Mark","value":"D-3"},{"name":"Mark","value":null},{"name":"External ID","value":"e37453ab-55ac-464e-96ef-b2d748a679fc-00093f ...etc
```

```
query GetInstancesOfConcreteMaterial($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup( elementGroupId: $elementGroupId filter: {query: $propertyFilter} pagination: {limit: 20} ) { results { id name referencedBy(name: "Type") { results { id name properties { results { name value } } } } } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3","propertyFilter":"('reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJkNjE3 or 'reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJlZA) and 'property.name.Element Context'==Type"}
```

```
{"data":{"elementsByElementGroup":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzExMTY","name":"Concrete 10","referencedBy":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3X2EzOTY3","name":"Concrete 10","properties":{"results":[{"name":"Comments","value":null},{"name":"Has Association","value":false},{"name":" ...etc
```

```
query GetConcreteMaterials($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup( elementGroupId: $elementGroupId filter: {query: $propertyFilter} pagination: {limit: 20} ) { results { id name } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVB","propertyFilter":"property.name.category==Materials and 'property.name.Element Name'=contains='Concrete'"}
```

```
{"data":{"elementsByElementGroup":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzE1Nzc0Mw","name":"Concrete, Precast Smooth, Light Grey"},{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzFmYjFhNA","name":"Concrete, Polished"},{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzQ5ZmI","name":" ...etc
```

```
query GetInstancesOfConcreteMaterial($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup(elementGroupId: $elementGroupId, filter: { query: $propertyFilter}, pagination : { limit : 20 }) { results { id name properties { results { name value } } references{ results{ name displayValue value{ properties{ results{ name value displayValue } } } } } } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3","propertyFilter":"('reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJkNjE3 or 'reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJlZA) and 'property.name.Element Context'==Instance"}
```

```
{"data":{"elementsByElementGroup":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzkzZjc1","name":"CC24x24","properties":{"results":[{"name":"Comments","value":null},{"name":"Has Association","value":false},{"name":"Column Location Mark","value":"D-3"},{"name":"Mark","value":null},{"name":"External ID","value":"e37453ab-55ac-464e-96ef-b2d748a679fc-00093f ...etc
```

```
query GetInstancesOfConcreteMaterial($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup( elementGroupId: $elementGroupId filter: {query: $propertyFilter} pagination: {limit: 20} ) { results { id name referencedBy(name: "Type") { results { id name properties { results { name value } } } } } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3","propertyFilter":"('reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJkNjE3 or 'reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJlZA) and 'property.name.Element Context'==Type"}
```

```
{"data":{"elementsByElementGroup":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzExMTY","name":"Concrete 10","referencedBy":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3X2EzOTY3","name":"Concrete 10","properties":{"results":[{"name":"Comments","value":null},{"name":"Has Association","value":false},{"name":" ...etc
```

## Pagination
```
query GetProjects($hubId: ID!) { projects(hubId: $hubId, pagination:{limit:3}) { pagination { cursor } results { id name alternativeIdentifiers{ externalProjectId } } } }
```

```
{"hubId":"b.03f98b13-ec95-461b-b945-765f496165c1"}
```

```
{"data":{"projects":{"pagination":{"cursor":"Y3Vyc34xfjM"},"results":[{"id":"YWltcHJvan5iLjAzZjk4YjEzLWVjOTUtNDYxYi1iOTQ1LTc2NWY0OTYxNjVjMX5iLjI1MTg2MzE1LWIyNWMtNDkxMC05MzkxLTllMGE4ZjhmNzA5Zg","name":"JM AEC Data Model Samples","alternativeIdentifiers":{"externalProjectId":"b.25186315-b25c-4910-9391-9e0a8f8f709f"}},{"id":"YWltcHJvan5iLjAzZjk4YjEzLWVjOTUtNDYxYi1iOTQ1LTc2NWY0OTYxNjVjMX5iLjg3OGIzMTkx ...etc
```

```
query GetProjects($hubId: ID!) { projects(hubId: $hubId, pagination:{cursor:"dXJuOmFkc2sud29ya3NwYWNlOnByb2QucHJvamVjdDo1NjZkOWNiNi0yOTA3LTRhOWQtYWU4OC0zYmI3Y2YyZjE4Yjd-Mw"}) { pagination { cursor } results { id name alternativeIdentifiers{ dataManagementAPIProjectId } } } }
```

```
{"hubId":"urn:adsk.ace:prod.scope:dccde3e3-c20c-40d3-a27c-7ac53b051b6e"}
```

```
{"data":{"projects":{"pagination":{"cursor":"dXJuOmFkc2sud29ya3NwYWNlOnByb2QucHJvamVjdDo2NDllNzQ2My0wZTc1LTRjMDMtOWM5Zi0zNDUwNzMzMzc4ZWN-Mw"},"results":[{"id":"urn:adsk.workspace:prod.project:566d9cb6-2907-4a9d-ae88-3bb7cf2f18b7","name":"Construction : Sample Project - Seaport Civic Center","alternativeIdentifiers":{"dataManagementAPIProjectId":"b.9177ea8c-efb4-4612-8ef1-6e4ce114658c"}},{"id":"urn ...etc
```

```
query GetProjects($hubId: ID!) { projects(hubId: $hubId, pagination:{limit:3}) { pagination { cursor } results { id name alternativeIdentifiers{ externalProjectId } } } }
```

```
{"hubId":"b.03f98b13-ec95-461b-b945-765f496165c1"}
```

```
{"data":{"projects":{"pagination":{"cursor":"Y3Vyc34xfjM"},"results":[{"id":"YWltcHJvan5iLjAzZjk4YjEzLWVjOTUtNDYxYi1iOTQ1LTc2NWY0OTYxNjVjMX5iLjI1MTg2MzE1LWIyNWMtNDkxMC05MzkxLTllMGE4ZjhmNzA5Zg","name":"JM AEC Data Model Samples","alternativeIdentifiers":{"externalProjectId":"b.25186315-b25c-4910-9391-9e0a8f8f709f"}},{"id":"YWltcHJvan5iLjAzZjk4YjEzLWVjOTUtNDYxYi1iOTQ1LTc2NWY0OTYxNjVjMX5iLjg3OGIzMTkx ...etc
```

```
query GetProjects($hubId: ID!) { projects(hubId: $hubId, pagination:{cursor:"dXJuOmFkc2sud29ya3NwYWNlOnByb2QucHJvamVjdDo1NjZkOWNiNi0yOTA3LTRhOWQtYWU4OC0zYmI3Y2YyZjE4Yjd-Mw"}) { pagination { cursor } results { id name alternativeIdentifiers{ dataManagementAPIProjectId } } } }
```

```
{"hubId":"urn:adsk.ace:prod.scope:dccde3e3-c20c-40d3-a27c-7ac53b051b6e"}
```

```
{"data":{"projects":{"pagination":{"cursor":"dXJuOmFkc2sud29ya3NwYWNlOnByb2QucHJvamVjdDo2NDllNzQ2My0wZTc1LTRjMDMtOWM5Zi0zNDUwNzMzMzc4ZWN-Mw"},"results":[{"id":"urn:adsk.workspace:prod.project:566d9cb6-2907-4a9d-ae88-3bb7cf2f18b7","name":"Construction : Sample Project - Seaport Civic Center","alternativeIdentifiers":{"dataManagementAPIProjectId":"b.9177ea8c-efb4-4612-8ef1-6e4ce114658c"}},{"id":"urn ...etc
```

## Get Element Instances of a Particular Type
```
query ($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup( elementGroupId: $elementGroupId filter: { query: $propertyFilter } pagination: {limit: 5} ) { pagination { cursor } results { id name properties { results { name value } } referencedBy(name: "Type") { pagination { cursor } results { id name alternativeIdentifiers { externalElementId } properties { results { name value } } } } } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVB","propertyFilter":"'property.name.category'=contains=Walls and 'property.name.Element Context'==Type and 'property.name.Element Name'=contains='Foundation - 24'"}
```

```
{"data":{"elementsByElementGroup":{"pagination":{"cursor":null},"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzEyYTFiNQ","name":"Foundation - 24\" Concrete","properties":{"results":[{"name":"Description","value":null},{"name":"Manufacturer","value":null},{"name":"Model","value":null},{"name":"Type Comments","value":null},{"name":"URL","value":null},{"na ...etc
```

```
query ($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup( elementGroupId: $elementGroupId filter: { query: $propertyFilter } pagination: {limit: 5} ) { pagination { cursor } results { id name properties { results { name value } } referencedBy(name: "Type") { pagination { cursor } results { id name alternativeIdentifiers { externalElementId } properties { results { name value } } } } } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVB","propertyFilter":"'property.name.category'=contains=Walls and 'property.name.Element Context'==Type and 'property.name.Element Name'=contains='Foundation - 24'"}
```

```
{"data":{"elementsByElementGroup":{"pagination":{"cursor":null},"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzEyYTFiNQ","name":"Foundation - 24\" Concrete","properties":{"results":[{"name":"Description","value":null},{"name":"Manufacturer","value":null},{"name":"Model","value":null},{"name":"Type Comments","value":null},{"name":"URL","value":null},{"na ...etc
```


##  Get Elements by using Instances or Reference


```
query GetConcreteMaterials($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup( elementGroupId: $elementGroupId filter: {query: $propertyFilter} pagination: {limit: 20} ) { results { id name } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVB","propertyFilter":"property.name.category==Materials and 'property.name.Element Name'=contains='Concrete'"}
```

```
{"data":{"elementsByElementGroup":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzE1Nzc0Mw","name":"Concrete, Precast Smooth, Light Grey"},{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzFmYjFhNA","name":"Concrete, Polished"},{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzQ5ZmI","name":" ...etc
```

```
query GetInstancesOfConcreteMaterial($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup(elementGroupId: $elementGroupId, filter: { query: $propertyFilter}, pagination : { limit : 20 }) { results { id name properties { results { name value } } references{ results{ name displayValue value{ properties{ results{ name value displayValue } } } } } } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3","propertyFilter":"('reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJkNjE3 or 'reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJlZA) and 'property.name.Element Context'==Instance"}
```

```
{"data":{"elementsByElementGroup":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzkzZjc1","name":"CC24x24","properties":{"results":[{"name":"Comments","value":null},{"name":"Has Association","value":false},{"name":"Column Location Mark","value":"D-3"},{"name":"Mark","value":null},{"name":"External ID","value":"e37453ab-55ac-464e-96ef-b2d748a679fc-00093f ...etc
```

```
query GetInstancesOfConcreteMaterial($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup( elementGroupId: $elementGroupId filter: {query: $propertyFilter} pagination: {limit: 20} ) { results { id name referencedBy(name: "Type") { results { id name properties { results { name value } } } } } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3","propertyFilter":"('reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJkNjE3 or 'reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJlZA) and 'property.name.Element Context'==Type"}
```

```
{"data":{"elementsByElementGroup":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzExMTY","name":"Concrete 10","referencedBy":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3X2EzOTY3","name":"Concrete 10","properties":{"results":[{"name":"Comments","value":null},{"name":"Has Association","value":false},{"name":" ...etc
```

```
query GetConcreteMaterials($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup( elementGroupId: $elementGroupId filter: {query: $propertyFilter} pagination: {limit: 20} ) { results { id name } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVB","propertyFilter":"property.name.category==Materials and 'property.name.Element Name'=contains='Concrete'"}
```

```
{"data":{"elementsByElementGroup":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzE1Nzc0Mw","name":"Concrete, Precast Smooth, Light Grey"},{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzFmYjFhNA","name":"Concrete, Polished"},{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ35yRWRKT0NPcVIwZWt5SkJCWWxSOUVBXzQ5ZmI","name":" ...etc
```

```
query GetInstancesOfConcreteMaterial($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup(elementGroupId: $elementGroupId, filter: { query: $propertyFilter}, pagination : { limit : 20 }) { results { id name properties { results { name value } } references{ results{ name displayValue value{ properties{ results{ name value displayValue } } } } } } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3","propertyFilter":"('reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJkNjE3 or 'reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJlZA) and 'property.name.Element Context'==Instance"}
```

```
{"data":{"elementsByElementGroup":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzkzZjc1","name":"CC24x24","properties":{"results":[{"name":"Comments","value":null},{"name":"Has Association","value":false},{"name":"Column Location Mark","value":"D-3"},{"name":"Mark","value":null},{"name":"External ID","value":"e37453ab-55ac-464e-96ef-b2d748a679fc-00093f ...etc
```

```
query GetInstancesOfConcreteMaterial($elementGroupId: ID!, $propertyFilter: String!) { elementsByElementGroup( elementGroupId: $elementGroupId filter: {query: $propertyFilter} pagination: {limit: 20} ) { results { id name referencedBy(name: "Type") { results { id name properties { results { name value } } } } } } }
```

```
{"elementGroupId":"YWVjZH42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3","propertyFilter":"('reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJkNjE3 or 'reference.Structural Material'==YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzJlZA) and 'property.name.Element Context'==Type"}
```

```
{"data":{"elementsByElementGroup":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3XzExMTY","name":"Concrete 10","referencedBy":{"results":[{"id":"YWVjZX42SUpGQXdONExWTG5JZXZiQk5GNU1IX0wyQ350OU0xX0J3VVRObVllbXRoUVBYNHh3X2EzOTY3","name":"Concrete 10","properties":{"results":[{"name":"Comments","value":null},{"name":"Has Association","value":false},{"name":" ...etc
```


## Get Distinct Values of Properties

```
query ($elementGroupId: ID!, $propertyDefinitionId: ID!, $filter: ElementFilterInput) { distinctPropertyValuesInElementGroupById(elementGroupId: $elementGroupId, propertyDefinitionId: $propertyDefinitionId, filter: $filter) { values(limit: 200) { value, count } } }
```

```
{"elementGroupId":"YWVjZH5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ35GZGhKOWZxZFJSR2QxTXAwNU1RWkVR","propertyDefinitionId":"autodesk.revit.parameter:parameter.category-2.0.0"}
```

```
"values": [ { "value": "Curtain Wall Mullions", "count": 2372 }, { "value": "Analytical Nodes", "count": 1410 } ]
```

```
query ($elementGroupId: ID!, $name: String!, $filter: ElementFilterInput, $pagination: PaginationInput) { distinctPropertyValuesInElementGroupByName(elementGroupId: $elementGroupId, name: $name, filter: $filter, pagination: $pagination) { pagination { cursor } results { definition { id } values(limit: 200) { value count } } } }
```

```
{"elementGroupId":"YWVjZH5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ35GZGhKOWZxZFJSR2QxTXAwNU1RWkVR","name":"Length"}
```

```
"results": [ { "definition": { "id": "autodesk.revit.parameter:structuralFoundationLength-2.0.0", }, "values": [ { "value": "1.93546015625", "count": 5 }, { "value": "1.0947796875000002", "count": 1 } ] }, { "definition": { "id": "autodesk.revit.parameter:continuousrailEndExtensionLengthParam-2.0.0", }, "values": [ { "value": "3.0463569792873577", "count": 1 } ] } }
```

```
{"elementGroupId":"YWVjZH5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ35GZGhKOWZxZFJSR2QxTXAwNU1RWkVR","name":"Family Name","filter":{"query":"property.name.category==Doors"}}
```

```
{"elementGroupId":"YWVjZH5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ35GZGhKOWZxZFJSR2QxTXAwNU1RWkVR","name":"Type","filter":{"query":"'property.name.Family Name'=='Single'"}}
```

```
{"elementGroupId":"YWVjZH5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ35GZGhKOWZxZFJSR2QxTXAwNU1RWkVR","name":"Structural Material","filter":{"query":"property.name.category==Walls"}}
```

```
{ "elementGroupId": "YWVjZH5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ35GZGhKOWZxZFJSR2QxTXAwNU1RWkVR", "name": "Width", "filter": { "query" : "property.name.category==Doors", "properties" { "name": "Width", "valueWithComparator": { "value": "0.9", "comparator": "LESS_THAN" } } } }
```

```
query ($elementGroupId: ID!, $propertyDefinitionId: ID!, $filter: ElementFilterInput) { distinctPropertyValuesInElementGroupById(elementGroupId: $elementGroupId, propertyDefinitionId: $propertyDefinitionId, filter: $filter) { values(limit: 200) { value, count } } }
```

```
{"elementGroupId":"YWVjZH5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ35GZGhKOWZxZFJSR2QxTXAwNU1RWkVR","propertyDefinitionId":"autodesk.revit.parameter:parameter.category-2.0.0"}
```

```
"values": [ { "value": "Curtain Wall Mullions", "count": 2372 }, { "value": "Analytical Nodes", "count": 1410 } ]
```

```
query ($elementGroupId: ID!, $name: String!, $filter: ElementFilterInput, $pagination: PaginationInput) { distinctPropertyValuesInElementGroupByName(elementGroupId: $elementGroupId, name: $name, filter: $filter, pagination: $pagination) { pagination { cursor } results { definition { id } values(limit: 200) { value count } } } }
```

```
{"elementGroupId":"YWVjZH5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ35GZGhKOWZxZFJSR2QxTXAwNU1RWkVR","name":"Length"}
```

```
"results": [ { "definition": { "id": "autodesk.revit.parameter:structuralFoundationLength-2.0.0", }, "values": [ { "value": "1.93546015625", "count": 5 }, { "value": "1.0947796875000002", "count": 1 } ] }, { "definition": { "id": "autodesk.revit.parameter:continuousrailEndExtensionLengthParam-2.0.0", }, "values": [ { "value": "3.0463569792873577", "count": 1 } ] } }
```

```
{"elementGroupId":"YWVjZH5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ35GZGhKOWZxZFJSR2QxTXAwNU1RWkVR","name":"Family Name","filter":{"query":"property.name.category==Doors"}}
```

```
{"elementGroupId":"YWVjZH5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ35GZGhKOWZxZFJSR2QxTXAwNU1RWkVR","name":"Type","filter":{"query":"'property.name.Family Name'=='Single'"}}
```

```
{"elementGroupId":"YWVjZH5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ35GZGhKOWZxZFJSR2QxTXAwNU1RWkVR","name":"Structural Material","filter":{"query":"property.name.category==Walls"}}
```

```
{ "elementGroupId": "YWVjZH5JR0JWdWROM2QxdW1kTkJZRnR2ZlpBX0wyQ35GZGhKOWZxZFJSR2QxTXAwNU1RWkVR", "name": "Width", "filter": { "query" : "property.name.category==Doors", "properties" { "name": "Width", "valueWithComparator": { "value": "0.9", "comparator": "LESS_THAN" } } } }
```