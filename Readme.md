## Content

This repository contains two `llm.txt` files:

* A condensed version of the official APS GraphQL `LLM.txt`, with the same content, without items that are not relevant to VIKTOR.
* A custom `llm.txt`, smaller, focused on VIKTOR and Python.

The types of prompts this custom LLM works best with are listed in the `Examples` folder.

## Limitations

* Queries between versions are not supported.
* Navigation queries are not supported, the Autodesk File Field and the `elementGroupId` method replace them.
* Queries across projects are not supported, queries are limited to a single `elementGroupId`.
* For distinct values, this repository focuses on “Retrieve distinct values by name”, instead of “Retrieve distinct values by id”, since queries are written in natural language.
  [https://aps.autodesk.com/en/docs/aecdatamodel/v1/tutorials/tutorial02/distinctvaluesquery/#retrieve-distinct-values-by-name](https://aps.autodesk.com/en/docs/aecdatamodel/v1/tutorials/tutorial02/distinctvaluesquery/#retrieve-distinct-values-by-name)

## Size
* `custom-aec-data-model-REV0.md`: 4,000 tokens
* `original-aec-data-model-llm-condense-REV0.md`: 10,100 tokens
