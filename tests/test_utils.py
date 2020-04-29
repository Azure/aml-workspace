import os
import sys
import pytest
import json

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, "..", "code"))

from utils import load_json, validate_json, AMLConfigurationException
from schema import azure_credentials_schema, azure_workspace_schema

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
    json_object = {
    "name": "<your-workspace-name>",
    "resource_group": "<your-resource-group-name>",
    "create_workspace": "false",
    "friendly_name": "<your-friendly-name>",
    "create_resource_group": "true",
    "location": "<your-workspace-location>",
    "sku": "<your-sku>",
    "storage_account": "Microsoft.Storage/storageAccounts/<your-storage-account-name>",
    "key_vault": "Microsoft.KeyVault/vaults/<your-key-vault-name>",
    "app_insights": "Microsoft.Insights/components/<your-app-insights-name>",
    "container_registry": "Microsoft.ContainerRegistry/registries/<your-container-registry-name>",
    "cmk_key_vault": "Microsoft.KeyVault/vaults/<your-key-vault-name>",
    "resource_cmk_uri": "https://<your-cmk-uri>",
    "hbi_workspace": "false"
}
    validate_json(
        data=json_object,
        schema=json.loads(azure_workspace_schema),
        input_name="PARAMETERS_FILE"
    )


def test_validate_json_invalid_json():
    """
    Unit test to check the validate_json function with invalid json_object inputs
    """
    json_object = {
        "sku": ""
    }
    with pytest.raises(AMLConfigurationException):
        assert validate_json(
            data=json_object,
            schema=json.loads(azure_credentials_schema),
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
