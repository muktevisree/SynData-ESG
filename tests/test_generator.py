# tests/test_generator.py

import os
import sys
import pytest

# Allow imports from parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.schema_parser import load_schema
from modules.generator import generate_records

def test_generate_records():
    schema = load_schema("presets/ghg.yaml")
    records = generate_records(schema, num_records=5, seed=123)

    assert len(records) == 5, "Should generate correct number of records"
    assert isinstance(records[0], dict), "Each record should be a dictionary"
    assert "facility_name" in records[0], "Expected field missing from record"
