import os
import sys
import pytest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, "..", "code"))

from utils import load_json, validate_json, AMLConfigurationException


def test_load_json_valid_input():
    """
    Unit test to check the load_json function with valid input
    """
    file_path = os.path.join(".cloud", ".azure", "workspace.json")
    json_object = load_json(
        file_path=file_path
    )
    assert type(json_object) == dict


def test_load_json_invalid_input():
    """
    Unit test to check the load_json function with invalid input
    """
    with pytest.raises(FileNotFoundError):
        assert load_json(
            file_path=""
        )


def test_validate_json():
    """
    Unit test to check the validate_json function
    """
    json_path = os.path.join(".cloud", ".azure", "workspace.json")
    schema_path = os.path.join("code", "schemas", "workspace_schema.json")
    json_object = load_json(
        file_path=json_path
    )
    schema_object = load_json(
        file_path=schema_path
    )
    with pytest.raises(AMLConfigurationException):
        assert validate_json(
            data=json_object,
            schema=schema_object,
            input_name="PARAMETERS_FILE"
        )
