import os
import json

from azureml.core import Workspace
from azureml.exceptions import WorkspaceException, AuthenticationException, ProjectSystemException
from azureml.core.authentication import ServicePrincipalAuthentication
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError
from utils import required_parameters_provided, AMLConfigurationException


def main():
    # Loading input values
    print("::debug::Loading input values")
    parameters_file = os.environ.get("INPUT_PARAMETERSFILE", default="workspace.json")
    azure_credentials = os.environ.get("INPUT_AZURECREDENTIALS", default="{}")
    try:
        azure_credentials = json.loads(azure_credentials)
        azure_credentials.get("tenantId")
        azure_credentials.get("clientId")
        azure_credentials.get("clientSecret")
        azure_credentials.get("subscriptionId")
    except JSONDecodeError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS. The JSON should include the following keys: 'tenantId', 'clientId', 'clientSecret' and 'subscriptionId'.")
        raise AMLConfigurationException(f"Incorrect or poorly formed output from azure login saved in AZURE_CREDENTIALS secret. See setup in https://github.com/Azure/aml-workspace/blob/master/README.md")

    # Loading parameters file
    print("::debug::Loading parameters file")
    parameters_file_path = os.path.join(".aml", ".azure", parameters_file)
    try:
        with open(parameters_file_path) as f:
            parameters = json.load(f)
    except FileNotFoundError:
        print(f"::error::Could not find parameter file in {parameters_file_path}. Please provide a parameter file in your repository (e.g. .ml/.azure/workspace.json).")
        raise AMLConfigurationException(f"Could not find parameter file in {parameters_file_path}. Please provide a parameter file in your repository (e.g. .ml/.azure/workspace.json).")
    
    # Checking if all required parameters were provided for loading a workspace
    required_parameters_provided(
        parameters=parameters,
        keys=["name", "resource_group"]
    )

    # Loading Workspace
    sp_auth = ServicePrincipalAuthentication(
        tenant_id=azure_credentials.get("tenantId", ""),
        service_principal_id=azure_credentials.get("clientId", ""),
        service_principal_password=azure_credentials.get("clientSecret", "")
    )
    try:
        print("::debug::Loading existing Workspace")
        ws = Workspace.get(
            name=parameters.get("name", None),
            subscription_id=azure_credentials.get("subscriptionId", ""),
            resource_group=parameters.get("resourceGroup", None),
            auth=sp_auth
        )
        print("::debug::Successfully loaded existing Workspace")
    except AuthenticationException as exception:
        print(f"::error::Could not retrieve user token. Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS: {exception}")
        raise AuthenticationException
    except AuthenticationError as exception:
        print(f"::error::Microsoft REST Authentication Error: {exception}")
        raise AuthenticationException
    except AdalError as exception:
        print(f"::error::Active Directory Authentication Library Error: {exception}")
        raise AdalError
    except ProjectSystemException as exception:
        print(f"::error::Workspace authorizationfailed: {exception}")
        raise ProjectSystemException
    except WorkspaceException as exception:
        print(f"::debug::Loading existing Workspace failed: {exception}")
        if parameters.get("createWorkspace", False):
            # Checking if all required parameters were provided for loading a workspace
            required_parameters_provided(
                parameters=parameters,
                keys=["name", "resource_group"]
            )
            try:
                print("::debug::Creating new Workspace")
                ws = Workspace.create(
                    name=parameters.get("name", None),
                    subscription_id=azure_credentials.get("subscriptionId", ""),
                    resource_group=parameters.get("resourceGroup", None),
                    location=parameters.get("location", None),
                    create_resource_group=parameters.get("createResourceGroup", False),
                    sku=parameters.get("sku", "basic"),
                    friendly_name=parameters.get("friendlyName", None),
                    storage_account=parameters.get("storageAccount", None),
                    key_vault=parameters.get("keyVault", None),
                    app_insights=parameters.get("appInsights", None),
                    container_registry=parameters.get("containerRegistry", None),
                    cmk_keyvault=parameters.get("cmkKeyVault", None),
                    resource_cmk_uri=parameters.get("resourceCmkUri", None),
                    hbi_workspace=parameters.get("hbiWorkspace", None),
                    auth=sp_auth,
                    exist_ok=True,
                    show_output=True
                )
            except WorkspaceException as exception:
                print(f"::error::Creating new Workspace failed: {exception}")
                raise WorkspaceException()

    # Write Workspace ARM properties to config file
    print("::debug::Writing Workspace ARM properties to config file")
    config_file_path = os.environ.get("GITHUB_WORKSPACE", default=".aml")
    config_file_name = "aml_arm_config.json"
    ws.write_config(
        path=config_file_path,
        file_name=config_file_name
    )
    print("::debug::Successfully finished Azure Machine Learning Workspace Action")


if __name__ == "__main__":
    main()
