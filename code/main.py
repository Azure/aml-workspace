import os
import json

from azureml.core import Workspace
from azureml.exceptions import WorkspaceException, AuthenticationException, ProjectSystemException
from azureml.core.authentication import ServicePrincipalAuthentication
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError
from utils import AMLConfigurationException, mask_parameter, validate_json
from schema import azure_credentials_schema, parameters_schema


def main():
    # Loading azure credentials
    print("::debug::Loading azure credentials")
    azure_credentials = os.environ.get("INPUT_AZURE_CREDENTIALS", default="{}")
    try:
        azure_credentials = json.loads(azure_credentials)
    except JSONDecodeError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS. The JSON should include the following keys: 'tenantId', 'clientId', 'clientSecret' and 'subscriptionId'.")
        raise AMLConfigurationException(f"Incorrect or poorly formed output from azure credentials saved in AZURE_CREDENTIALS secret. See setup in https://github.com/Azure/aml-workspace/blob/master/README.md")

    # Checking provided parameters
    print("::debug::Checking provided parameters")
    validate_json(
        data=azure_credentials,
        schema=azure_credentials_schema,
        input_name="AZURE_CREDENTIALS"
    )

    # Mask values
    print("::debug::Masking parameters")
    mask_parameter(parameter=azure_credentials.get("tenantId", ""))
    mask_parameter(parameter=azure_credentials.get("clientId", ""))
    mask_parameter(parameter=azure_credentials.get("clientSecret", ""))
    mask_parameter(parameter=azure_credentials.get("subscriptionId", ""))

    # Loading parameters file
    print("::debug::Loading parameters file")
    parameters_file = os.environ.get("INPUT_PARAMETERS_FILE", default="workspace.json")
    parameters_file_path = os.path.join(".cloud", ".azure", parameters_file)
    try:
        with open(parameters_file_path) as f:
            parameters = json.load(f)
    except FileNotFoundError:
        print(f"::debug::Could not find parameter file in {parameters_file_path}. Please provide a parameter file in your repository if you do not want to use default settings (e.g. .cloud/.azure/workspace.json).")
        parameters = {}

    # Checking provided parameters
    print("::debug::Checking provided parameters")
    validate_json(
        data=parameters,
        schema=parameters_schema,
        input_name="PARAMETERS_FILE"
    )

    # Loading Workspace
    sp_auth = ServicePrincipalAuthentication(
        tenant_id=azure_credentials.get("tenantId", ""),
        service_principal_id=azure_credentials.get("clientId", ""),
        service_principal_password=azure_credentials.get("clientSecret", "")
    )
    try:
        print("::debug::Loading existing Workspace")
        # Default workspace and resource group name
        repository_name = str(os.environ.get("GITHUB_REPOSITORY")).split("/")[-1]

        ws = Workspace.get(
            name=parameters.get("name", repository_name),
            subscription_id=azure_credentials.get("subscriptionId", ""),
            resource_group=parameters.get("resource_group", repository_name),
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
        if parameters.get("create_workspace", False):
            try:
                print("::debug::Creating new Workspace")
                ws = Workspace.create(
                    name=parameters.get("name", repository_name),
                    subscription_id=azure_credentials.get("subscriptionId", ""),
                    resource_group=parameters.get("resource_group", repository_name),
                    location=parameters.get("location", None),
                    create_resource_group=parameters.get("create_resource_group", True),
                    sku=parameters.get("sku", "basic"),
                    friendly_name=parameters.get("friendly_name", None),
                    storage_account=parameters.get("storage_account", None),
                    key_vault=parameters.get("key_vault", None),
                    app_insights=parameters.get("app_insights", None),
                    container_registry=parameters.get("container_registry", None),
                    cmk_keyvault=parameters.get("cmk_key_vault", None),
                    resource_cmk_uri=parameters.get("resource_cmk_uri", None),
                    hbi_workspace=parameters.get("hbi_workspace", None),
                    auth=sp_auth,
                    exist_ok=True,
                    show_output=True
                )
            except WorkspaceException as exception:
                print(f"::error::Creating new Workspace failed: {exception}")
                raise AMLConfigurationException(f"Creating new Workspace failed with 'WorkspaceException': {exception}.")
        else:
            print(f"::error::Loading existing Workspace failed with 'WorkspaceException' and new Workspace will not be created because parameter 'create_workspace' was not defined or set to false in your parameter file: {exception}")
            raise AMLConfigurationException("Loading existing Workspace failed with 'WorkspaceException' and new Workspace will not be created because parameter 'create_workspace' was not defined or set to false in your parameter file.")

    # Write Workspace ARM properties to config file
    print("::debug::Writing Workspace ARM properties to config file")
    config_file_path = os.environ.get("GITHUB_WORKSPACE", default=".cloud/.azure")
    config_file_name = "aml_arm_config.json"
    ws.write_config(
        path=config_file_path,
        file_name=config_file_name
    )
    print("::debug::Successfully finished Azure Machine Learning Workspace Action")


if __name__ == "__main__":
    main()
