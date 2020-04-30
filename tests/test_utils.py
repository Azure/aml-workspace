import os
import sys
import pytest
import json

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, "..", "code"))

from utils import validate_json, AMLConfigurationException
from schemas import azure_credentials_schema, parameters_schema


def test_validate_json_valid_inputs():
    """
    Unit test to check the validate_json function with valid inputs
    """
    json_object = {
        "name": "workspace-name",
        "resource_group": "resource-group-name",
        "create_workspace": False,
        "friendly_name": "friendly-name",
        "create_resource_group": True,
        "location": "location",
        "sku": "basic",
        "storage_account": "Microsoft.Storage/storageAccounts/<your-storage-account-name>",
        "key_vault": "Microsoft.KeyVault/vaults/<your-key-vault-name>",
        "app_insights": "Microsoft.Insights/components/<your-app-insights-name>",
        "container_registry": "Microsoft.ContainerRegistry/registries/<your-container-registry-name>",
        "cmk_key_vault": "Microsoft.KeyVault/vaults/<your-key-vault-name>",
        "resource_cmk_uri": "https://<your-cmk-uri>",
        "hbi_workspace": False
    }
    validate_json(
        data=json_object,
        schema=parameters_schema,
        input_name="PARAMETERS_FILE"
    )


def test_validate_json_incorrect_field():
    """
    Unit test to check if field incorrect
    """
    json_object = {
        "name": "workspace-name",
        "resour_group": "resource-group-name",
    }
    with pytest.raises(AMLConfigurationException):
        assert validate_json(
            data=json_object,
            schema=azure_credentials_schema,
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
            schema=azure_credentials_schema,
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
