# JSON-Explore

A lightweight CLI tool for interactively exploring JSON files and dictionaries.

## Installation

Install using pip:
```bash
pip install json-explore
```

## Import Instructions

```python
import json_explore
```

## Usage

```python
import json_explore

json_example: dict = \
{"menu": {
  "id": 29,
  "value": "File",
  "popup": {
    "menuitem": [
      {"value": "New", "onclick": "CreateNewDoc()"},
      {"value": "Open", "onclick": "OpenDoc()"},
      {"value": "Close", "onclick": "CloseDoc()"}
    ]
  }
}}
print(f"Let's explore the above json using the json explore function")
print()
json_explore.json_explore_json(json_example)

print(f"Now lets explore the same json using the file path function")
print()
json_explore.json_explore_fp("test.json")
```

## CLI example
```bash
json-explore path/to/your/file.json
```

## Navigation
Enter a key name or an element number to navigate into a that json level
Enter a ^ to navigate up
Enter Q to quit

When at the top the JSON level name will be Top

## Example

```text
Q to quit
^ to go up
Type key string or element number to go into lower level

JSON level: Top dict:
	menu: dict

:menu
JSON level: menu dict:
	id: 29: <class 'int'>
	value: File: <class 'str'>
	popup: dict

:popup
JSON level: popup dict:
	menuitem: list

:menuitem
JSON level: menuitem list:
	Element: 0: dict
	Element: 1: dict
	Element: 2: dict

:1
JSON level: 1 dict:
	value: Open: <class 'str'>
	onclick: OpenDoc(): <class 'str'>

:^
JSON level: menuitem list:
	Element: 0: dict
	Element: 1: dict
	Element: 2: dict

:^
JSON level: popup dict:
	menuitem: list

:Q
```