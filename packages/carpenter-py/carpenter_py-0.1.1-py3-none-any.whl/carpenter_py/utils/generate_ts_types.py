import json
import re
from pathlib import Path
from typing import Set

# Mapping Python type strings to TypeScript equivalents
PY_TO_TS_TYPE = {
    "str": "string",
    "int": "number",
    "float": "number",
    "bool": "boolean",
    "list": "any[]",
    "dict": "Record<string, any>",
    "tuple": "any[]",
    "None": "void",
    "Any": "any",
    "Optional": "null | any",
    "Union": "any",
    "Literal": "string | number | boolean",
}

# Complex type pattern matching
LIST_PATTERN = re.compile(r"list\[(.*)\]")
DICT_PATTERN = re.compile(r"dict\[(.*),\s*(.*)\]")
UNION_PATTERN = re.compile(r"Union\[(.*)\]")
OPTIONAL_PATTERN = re.compile(r"Optional\[(.*)\]")
LITERAL_PATTERN = re.compile(r"Literal\[(.*)\]")
TUPLE_PATTERN = re.compile(r"tuple\[(.*)\]")


def parse_complex_type(py_type: str) -> str:
    """Parse complex Python types like list[str], dict[str, int], etc."""
    # Handle list[...]
    list_match = LIST_PATTERN.match(py_type)
    if list_match:
        inner_type = convert_type(list_match.group(1))
        return f"Array<{inner_type}>"

    # Handle dict[K, V]
    dict_match = DICT_PATTERN.match(py_type)
    if dict_match:
        key_type = convert_type(dict_match.group(1))
        val_type = convert_type(dict_match.group(2))
        if key_type == "string":
            return f"Record<string, {val_type}>"
        else:
            return f"Map<{key_type}, {val_type}>"

    # Handle Union[A, B, C]
    union_match = UNION_PATTERN.match(py_type)
    if union_match:
        inner_types = union_match.group(1).split(",")
        ts_types = [convert_type(t.strip()) for t in inner_types]
        return " | ".join(ts_types)

    # Handle Optional[T]
    optional_match = OPTIONAL_PATTERN.match(py_type)
    if optional_match:
        inner_type = convert_type(optional_match.group(1))
        return f"{inner_type} | null | undefined"

    # Handle Literal[A, B, C]
    literal_match = LITERAL_PATTERN.match(py_type)
    if literal_match:
        literals = literal_match.group(1).split(",")
        # Process literals and wrap strings in quotes
        processed_literals = []
        for lit in literals:
            lit = lit.strip()
            if lit.startswith('"') or lit.startswith("'"):
                # Already quoted
                processed_literals.append(lit)
            elif lit.lower() in ("true", "false", "none", "null"):
                # Boolean or null literals
                processed_literals.append(lit.lower())
            elif lit.isdigit() or (lit.startswith("-") and lit[1:].isdigit()):
                # Numbers
                processed_literals.append(lit)
            else:
                # Assume it's a string and quote it
                processed_literals.append(f'"{lit}"')
        return " | ".join(processed_literals)

    # Handle tuple[A, B, C]
    tuple_match = TUPLE_PATTERN.match(py_type)
    if tuple_match:
        inner_types = tuple_match.group(1).split(",")
        ts_types = [convert_type(t.strip()) for t in inner_types]
        return f"[{', '.join(ts_types)}]"

    return None


def convert_type(py_type: str) -> str:
    """Convert Python type annotation to TypeScript type."""
    py_type = py_type.strip()

    # Try to match complex types first
    complex_type = parse_complex_type(py_type)
    if complex_type:
        return complex_type

    # Use mapping for simple types
    return PY_TO_TS_TYPE.get(py_type, py_type)


def generate_ts_interface(name: str, fields: dict, generated_types: Set[str]) -> str:
    """Generate TypeScript interface definition from field data."""
    if not fields:
        type_def = f"export type {name} = {{}};\n"
        generated_types.add(name)
        return type_def

    lines = [f"export interface {name} {{"]
    for key, value in fields.items():
        # Handle optional properties (ending with '?')
        is_optional = False
        if key.endswith("?"):
            key = key[:-1]  # Remove the '?' character
            is_optional = True

        ts_type = convert_type(value)
        optional_marker = "?" if is_optional else ""
        lines.append(f"  {key}{optional_marker}: {ts_type};")

    lines.append("}\n")
    generated_types.add(name)
    return "\n".join(lines)


def generate_action_map(actions: dict) -> str:
    """Generate TypeScript ActionTypeMap from action metadata."""
    lines = ["declare module '@carpenter/actions' {", "  interface ActionTypeMap {"]

    for path, meta in actions.items():
        action_key = f'"{path}"'
        input_type = meta["input"]["type"]
        output_type = meta["output"]["type"]

        # For empty input or output, use appropriate types
        input_ts_type = input_type if meta["input"]["fields"] else "{}"
        output_ts_type = "void" if output_type == "None" else output_type

        lines.append(
            f"    {action_key}: {{ input: {input_ts_type}; output: {output_ts_type}; }};"
        )

    lines.append("  }")
    lines.append("}")
    return "\n".join(lines)


def generate_typescript_types(
    json_path: str = "action_map.json",
    output_path: str = "types/actions.d.ts",
    package_name: str = "@carpenter/actions",
):
    """Generate TypeScript type definitions from action map JSON."""
    try:
        with open(json_path) as f:
            action_map = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_path} not found")
        return
    except json.JSONDecodeError:
        print(f"Error: {json_path} contains invalid JSON")
        return

    output_path = Path(output_path)

    # Keep track of generated types to avoid duplicates
    generated_types = set()
    interfaces = []

    # Process all input and output types
    for _, meta in action_map.items():
        input_type = meta["input"]
        output_type = meta["output"]

        if input_type["fields"]:
            interfaces.append(
                generate_ts_interface(
                    input_type["type"], input_type["fields"], generated_types
                )
            )
        if output_type["type"] != "None" and output_type["fields"]:
            interfaces.append(
                generate_ts_interface(
                    output_type["type"], output_type["fields"], generated_types
                )
            )

    # Generate the file content
    ts = "// Auto-generated from action_map.json\n"
    ts += f"// Generated on {Path(json_path).stat().st_mtime}\n\n"

    # Add package import
    if package_name:
        ts += f'import {{ ActionTypeMap }} from "{package_name}";\n\n'

    # Add type definitions
    if interfaces:
        ts += "// Type definitions\n"
        ts += "\n".join(interfaces)
        ts += "\n\n"

    # Add action map
    ts += "// Action type mapping\n"
    ts += generate_action_map(action_map)

    # Ensure directory exists
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    output_path.write_text(ts)
