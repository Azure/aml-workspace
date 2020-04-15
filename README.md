![Integration Test](https://github.com/Azure/aml-workspace/workflows/Integration%20Test/badge.svg)
![Lint](https://github.com/Azure/aml-workspace/workflows/Lint/badge.svg)


# Azure Machine Learning Workspace Action

## Usage

The Azure Machine Learning Workspace action will allow you to create or connect to a Azure Machine Learning workspace so you can later run your Machine Learning experiments remotely, create production endpoints etc. If the workspace exists, it will connect to it, otherwise the action can create a new workspace based on the provided parameters. You will need to provide azure credentials that allow you to create and/or connect to a workspace. The action will output a config file that needs to be passed to the next AML actions if you are looking to chain more than one AML action together.

## Template repositories

This action is one in a series of actions that can be used to setup an ML Ops process. Examples of these can be found at
1. Simple example: [ml-template-azure](https://github.com/machine-learning-apps/ml-template-azure) and
2. Comprehensive example: [aml-template](https://github.com/Azure/aml-template).

### Example workflow

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
    - name: Check Out Repository
      id: checkout_repository
      uses: actions/checkout@v2

    # AML Workspace Action
    - uses: Azure/aml-workspace
      id: aml_workspace
      # required inputs as secrets
      with:
        # required
        azure_credentials: ${{ secrets.AZURE_CREDENTIALS }}
        # optional
        parameters_file: "workspace.json"
```

### Inputs

| Input | Required | Default | Description |
| ----- | -------- | ------- | ----------- |
| azure_credentials | x | - | Output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth`. This should be stored in your secrets |
| parameters_file |  | `"workspace.json"` | JSON file in the `.cloud/.azure` folder specifying your Azure Machine Learning Workspace details. |

#### Azure Credentials

Install the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) on your computer or use the Cloud CLI and execute the following command to generate the required credentials:

```sh
# Replace {service-principal-name}, {subscription-id} and {resource-group} with your Azure subscription id and resource group name and any name for your service principle
az ad sp create-for-rbac --name {service-principal-name} \
                         --role contributor \
                         --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
                         --sdk-auth
```

This will generate the following JSON output:

```sh
{
  "clientId": "<GUID>",
  "clientSecret": "<GUID>",
  "subscriptionId": "<GUID>",
  "tenantId": "<GUID>",
  (...)
}
```

Add this JSON output as [a secret](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets#creating-encrypted-secrets) with the name `AZURE_CREDENTIALS` in your GitHub repository.

#### Parameters File

The action tries to load a JSON file in the `.cloud/.azure` folder in your repository, which specifies details of your Azure Machine Learning Workspace. By default, the action expects a file with the name `workspace.json`. If your JSON file has a different name, you can specify it with this input parameter. Note that none of these values are required and in the absence, defaults will be created with the repo name.

A sample file can be found in this repository in the folder `.cloud/.azure`. The JSON file can include the following parameters:

| Parameter           | Required | Allowed Values                           | Default    | Description |
| ------------------- | -------- | ---------------------------------------- | ---------- | ----------- |
| name                | x        | str                                      | <REPOSITORY_NAME> | The workspace name. The name must be between 2 and 32 characters long. The first character of the name must be alphanumeric (letter or number), but the rest of the name may contain alphanumerics, hyphens, and underscores. Whitespace is not allowed. |
| resource_group       | x        | str                                      | <REPOSITORY_NAME> | The Azure resource group that contains the workspace. |
| create_workspace     | (only for creating) | bool                   | false      | Indicates whether to create the workspace if it doesn't exist. |
| friendly_name        |          | str                                      | null       | A friendly name for the workspace that can be displayed in the UI. |
| create_resource_group |          | bool                     | false       | Indicates whether to create the resource group if it doesn't exist. |
| location            |          | str: [supported region](https://azure.microsoft.com/global-infrastructure/services/?products=machine-learning-service) | resource group location | The location of the workspace. The parameter defaults to the resource group location. |
| sku                 |          | str: "basic", "enterprise"               | `"basic"`    | The SKU name (also referred as edition). |
| storage_account      |          | str: Azure resource ID format            | null       | An existing storage account in the Azure resource ID format (see example JSON file in `.cloud/.azure`). The storage will be used by the workspace to save run outputs, code, logs etc. If None, a new storage account will be created. |
| key_vault            |          | str: Azure resource ID format            | null       | An existing key vault in the Azure resource ID format (see example JSON file in `.cloud/.azure`). The key vault will be used by the workspace to store credentials added to the workspace by the users. If None, a new key vault will be created. |
| app_insights         |          | str: Azure resource ID format            | null       | An existing Application Insights in the Azure resource ID format (see example JSON file in `.cloud/.azure`). The Application Insights will be used by the workspace to log webservices events. If None, a new Application Insights will be created. |
| container_registry   |          | str: Azure resource ID format            | null       | An existing container registry in the Azure resource ID format (see example JSON file in `.cloud/.azure`). The container registry will be used by the workspace to pull and push both experimentation and webservices images. If None, a new container registry will be created only when needed and not along with workspace creation. |
| cmk_key_vault         |          | str: Azure resource ID format            | null       | The key vault containing the customer managed key in the Azure resource ID format (see example JSON file in `.cloud/.azure`). |
| resource_cmk_uri      |          | str: key URI of the customer managed key | null       | The key URI of the customer managed key to encrypt the data at rest (see example JSON file in `.cloud/.azure`). |
| hbi_workspace        |          | bool                       | false      | Specifies whether the customer data is of High Business Impact(HBI), i.e., contains sensitive business information. The default value is False. When set to True, downstream services will selectively disable logging. |

Please visit [this website](https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.workspace(class)?view=azure-ml-py#create-name--auth-none--subscription-id-none--resource-group-none--location-none--create-resource-group-true--sku--basic---friendly-name-none--storage-account-none--key-vault-none--app-insights-none--container-registry-none--cmk-keyvault-none--resource-cmk-uri-none--hbi-workspace-false--default-cpu-compute-target-none--default-gpu-compute-target-none--exist-ok-false--show-output-true-) for more details.

### Outputs

The action writes the workspace Azure Resource Manager (ARM) properties to a config file, which will be used by all other Azure Machine Learning GitHub Actions to interact with the workspace.

| Output Path                            | Description                                                             |
|--------------------------------------- | ----------------------------------------------------------------------- |
| `GITHUB_WORKSPACE/aml_arm_config.json` | configurations to be passed to additional steps for using the workspace |

### Other Azure Machine Learning Actions

- [aml-workspace](https://github.com/Azure/aml-workspace) - Connects to or creates a new workspace
- [aml-compute](https://github.com/Azure/aml-compute) - Connects to or creates a new compute target in Azure Machine Learning
- [aml-run](https://github.com/Azure/aml-run) - Submits a ScriptRun, an Estimator or a Pipeline to Azure Machine Learning
- [aml-registermodel](https://github.com/Azure/aml-registermodel) - Registers a model to Azure Machine Learning
- [aml-deploy](https://github.com/Azure/aml-deploy) - Deploys a model and creates an endpoint for the model

### Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

