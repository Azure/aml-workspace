![Integration Test](https://github.com/Azure/aml-workspace/workflows/Integration%20Test/badge.svg?branch=master&event=push)
![Lint and Test](https://github.com/Azure/aml-workspace/workflows/Lint%20and%20Test/badge.svg?branch=master&event=push)


# GitHub Action for creating or connecting to Azure Machine Learning Workspace

## Deprecation notice

This Action is deprecated. Instead, consider using the [CLI (v2)](https://docs.microsoft.com/azure/machine-learning/how-to-configure-cli) to manage and interact with Azure Machine Learning workspaces in GitHub Actions.

**Important:** The CLI (v2) is not recommended for production use while in preview.

## Usage

The aml-workspace action will login / connect to [Azure Machine Learning](https://azure.microsoft.com/en-us/services/machine-learning/).

Get started today with a [free Azure account](https://azure.com/free/open-source)!

This repository contains a GitHub Action for connecting to an Azure Machine Learning workspace. You can later use this context to train your model remotely, deploy your models to endpoints etc. You can also use this action to create a new workspace, if you provide the appropriate parameters. 


## Utilize GitHub Actions and Azure Machine Learning to train and deploy a machine learning model

This action is one in a series of actions that can be used to setup an ML Ops process. **We suggest getting started with one of our template repositories**, which will allow you to create an ML Ops process in less than 5 minutes.

1. **Simple template repository: [ml-template-azure](https://github.com/machine-learning-apps/ml-template-azure)**

    Go to this template and follow the getting started guide to setup an ML Ops process within minutes and learn how to use the Azure Machine Learning GitHub Actions in combination. This template demonstrates a very simple process for training and deploying machine learning models.

2. **Advanced template repository: [mlops-enterprise-template](https://github.com/Azure-Samples/mlops-enterprise-template)**

    This template demonstrates how the actions can be extended to include the normal pull request approval process and how training and deployment workflows can be split. More enhancements will be added to this template in the future to make it more enterprise ready.
    
    
## Example workflow for creating or connecting to Azure Machine Learning Workspace


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
    - uses: Azure/aml-workspace@v1
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
| parameters_file |  | `"workspace.json"` | We expect a JSON file in the `.cloud/.azure` folder in root of your repository specifying your Azure Machine Learning Workspace details. If you have want to provide these details in a file other than "workspace.json" you need to provide this input in the action. |

#### azure_credentials ( Azure Credentials ) 

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

#### parameters_file (Parameters File)

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

The action writes the workspace Azure Resource Manager (ARM) properties to a config file, which will be implicitly picked by all Azure Machine Learning GitHub Actions following this one, to interact with the workspace.

| Output Path                            | Description                                                             |
|--------------------------------------- | ----------------------------------------------------------------------- |
| `GITHUB_WORKSPACE/aml_arm_config.json` | configurations to be passed to additional steps for using the workspace |

### Other Azure Machine Learning Actions

- [aml-workspace](https://github.com/Azure/aml-workspace) - Connects to or creates a new workspace
- [aml-compute](https://github.com/Azure/aml-compute) - Connects to or creates a new compute target in Azure Machine Learning
- [aml-run](https://github.com/Azure/aml-run) - Submits a ScriptRun, an Estimator or a Pipeline to Azure Machine Learning
- [aml-registermodel](https://github.com/Azure/aml-registermodel) - Registers a model to Azure Machine Learning
- [aml-deploy](https://github.com/Azure/aml-deploy) - Deploys a model and creates an endpoint for the model

### Known issues

#### Error: MissingSubscriptionRegistration

Error message: 
```sh
Message: ***'error': ***'code': 'MissingSubscriptionRegistration', 'message': "The subscription is not registered to use namespace 'Microsoft.KeyVault'. See https://aka.ms/rps-not-found for how to register subscriptions.", 'details': [***'code': 'MissingSubscriptionRegistration', 'target': 'Microsoft.KeyVault', 'message': "The subscription is not registered to use namespace 'Microsoft.KeyVault'. See https://aka.ms/rps-not-found for how to register subscriptions
```
Solution:

This error message appears, in case the `Azure/aml-workspace` action tries to create a new Azure Machine Learning workspace in your resource group and you have never deployed a Key Vault in the subscription before. We recommend to create an Azure Machine Learning workspace manually in the Azure Portal. Follow the [steps on this website](https://docs.microsoft.com/en-us/azure/machine-learning/tutorial-1st-experiment-sdk-setup#create-a-workspace) to create a new workspace with the desired name. After ou have successfully completed the steps, you have to make sure, that your Service Principal has access to the resource group and that the details in your <a href="/.cloud/.azure/workspace.json">`/.cloud/.azure/workspace.json"` file</a> are correct and point to the right workspace and resource group.

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
