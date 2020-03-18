# Azure Machine Learning Workspace Action


## Usage

Description.

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

    steps:
    - uses: actions/checkout@master
    - name: Run action

      # Put your action repo here
      uses: me/myaction@master

      # Put an example of your mandatory inputs here
      with:
        myInput: world
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myInput`  | An example mandatory input    |
| `anotherInput` _(optional)_  | An example optional input    |

#### Parameter File

A sample file can be found in this repository in the folder `.aml`. The action expects a similar parameter file in your repository in the `.aml folder`.

| Parameter Name      | Required | Allowed Values                           | Default    | Description |
| ------------------- | -------- | ---------------------------------------- | ---------- |
| name                | x        | str                                      | no default | For more details please read [here](https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.workspace.workspace?view=azure-ml-py#create-name--auth-none--subscription-id-none--resource-group-none--location-none--create-resource-group-true--sku--basic---friendly-name-none--storage-account-none--key-vault-none--app-insights-none--container-registry-none--cmk-keyvault-none--resource-cmk-uri-none--hbi-workspace-false--default-cpu-compute-target-none--default-gpu-compute-target-none--exist-ok-false--show-output-true-) |
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
| `myOutput`  | An example output (returns 'Hello world')    |

## Examples



### Using the optional input

This is how to use the optional input.

```yaml
with:
  myInput: world
  anotherInput: optional
```

### Using outputs

Show people how to use your outputs in another action.

```yaml
steps:
- uses: actions/checkout@master
- name: Run action
  id: myaction

  # Put your action name here
  uses: me/myaction@master

  # Put an example of your mandatory arguments here
  with:
    myInput: world

# Put an example of using your outputs here
- name: Check outputs
    run: |
    echo "Outputs - ${{ steps.myaction.outputs.myOutput }}"
```