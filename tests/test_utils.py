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


def test_validate_json_valid_inputs():
    """
    Unit test to check the validate_json function with valid inputs
    """
    json_object = {}
    schema_path = os.path.join("schema", "workspace_schema.json")
    schema_object = load_json(
        file_path=schema_path
    )
    validate_json(
        data=json_object,
        schema=schema_object,
        input_name="PARAMETERS_FILE"
    )


def test_validate_json_invalid_json():
    """
    Unit test to check the validate_json function with invalid json_object inputs
    """
    json_object = {
        "sku": ""
    }
    schema_path = os.path.join("schema", "workspace_schema.json")
    schema_object = load_json(
        file_path=schema_path
    )
    with pytest.raises(AMLConfigurationException):
        assert validate_json(
            data=json_object,
            schema=schema_object,
            input_name="PARAMETERS_FILE"
        )


def test_validate_json_invalid_schema():
    """
    Unit test to check the validate_json function with invalid schema inputs
    """
    json_object = {}
    schema_object = {}
    with pytest.raises(Exception):
        assert validate_json(
            data=json_object,
            schema=schema_object,
            input_name="PARAMETERS_FILE"
        )
