# Azure Machine Learning Workspace Action

## Usage

The Azure Machine Learning Workspace action will allow you to connect to a remote workspace so you can later run your Machine Learning experiments remotely, create production endpoints etc. If the workspace exists, it will connect to it, otherwise the action will create a new workspace. You will need to have azure credentials that allow you to create and/or connect to a workspace. The action will output a config file that needs to be passed to the next AML actions if you are looking to chain more than one AML action together.

### Example workflow

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - name: Run action

      # AML Workspace Action
    - uses: azure/AMLWorkspace@master
      # required inputs as secrets
      with:
        azureCredentials: ${{ secrets.AZURE_CREDENTIALS }}
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `AZURE_CREDENTIALS`  | Output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth`. This should be stored in your secrets    |

#### Parameter File

A sample file can be found in this repository in the folder `.aml`. The action expects a similar parameter file in your repository in the `.aml folder`.

| Parameter Name      | Required | Allowed Values                           | Default    | Description |
| ------------------- | -------- | ---------------------------------------- | ---------- | ----------- |
| name                | x        | str                                      | no default | For more details please read [here](https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.workspace.workspace?view=azure-ml-py#create-name--auth-none--subscription-id-none--resource-group-none--location-none--create-resource-group-true--sku--basic---friendly-name-none--storage-account-none--key-vault-none--app-insights-none--container-registry-none--cmk-keyvault-none--resource-cmk-uri-none--hbi-workspace-false--default-cpu-compute-target-none--default-gpu-compute-target-none--exist-ok-false--show-output-true-) |
| resourceGroup       | x        | str                                      | no default |             |
| createWorkspace     |          | bool: true, false                        | false      | Create Workspace if it could not be loaded |
| friendlyName        |          | str                                      | null       |
| createResourceGroup |          | bool: true, false                        | null       |
| location            |          | str: [supported region](https://azure.microsoft.com/global-infrastructure/services/?products=machine-learning-service) | resource group location |
| sku                 |          | str: "basic", "enterprise"               | "basic"    |
| storageAccount      |          | str: Azure resource ID format            | null       |
| keyVault            |          | str: Azure resource ID format            | null       |
| appInsights         |          | str: Azure resource ID format            | null       |
| containerRegistry   |          | str: Azure resource ID format            | null       |
| cmkKeyVault         |          | str: Azure resource ID format            | null       |
| resourceCmkUri      |          | str: key URI of the customer managed key | null       |
| hbiWorkspace        |          | bool: true, false                        | false      |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `azureml/aml_arm_config.json`  | configurations to be passed to additional steps for using the workspace    |
