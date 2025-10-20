# modules/schema_parser.py

import yaml

def load_schema(schema_path):
    """
    Loads and parses the YAML schema file.

    Args:
        schema_path (str): Path to the YAML schema file.

    Returns:
        dict: Parsed schema as a Python dictionary.
    """
    try:
        with open(schema_path, 'r') as f:
            schema = yaml.safe_load(f)
        return schema
    except Exception as e:
        raise RuntimeError(f"Failed to load schema from {schema_path}: {e}")
