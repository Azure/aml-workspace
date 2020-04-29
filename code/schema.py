azure_credentials_schema ={
    "$id": "http://azure-ml.com/schemas/azure_credentials.json",
    "$schema": "http://json-schema.org/schema",
    "title": "azure_credentials",
    "description": "JSON specification for your azure credentials",
    "type": "object",
    "required": ["clientId", "clientSecret", "subscriptionId", "tenantId"],
    "properties": {
        "clientId": {
            "type": "string",
            "description": "The client ID of the service principal."
        },
        "clientSecret": {
            "type": "string",
            "description": "The client secret of the service principal."
        },
        "subscriptionId": {
            "type": "string",
            "description": "The subscription ID that should be used."
        },
        "tenantId": {
            "type": "string",
            "description": "The tenant ID of the service principal."
        }
    }
}

parameters_schema = {
    "$id": "http://azure-ml.com/schemas/workspace.json",
    "$schema": "http://json-schema.org/schema",
    "title": "aml-workspace",
    "description": "JSON specification for your workspace details",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "The workspace name.",
            "minLength": 2,
            "maxLength": 32
        },
        "resource_group": {
            "type": "string",
            "description": "The Azure resource group that contains the workspace."
        },
        "create_workspace": {
            "type": "boolean",
            "description": "Indicates whether to create the workspace if it doesn't exist."
        },
        "friendly_name": {
            "type": "string",
            "description": "A friendly name for the workspace that can be displayed in the UI."
        },
        "create_resource_group": {
            "type": "boolean",
            "description": "Indicates whether to create the resource group if it doesn't exist."
        },
        "location": {
            "type": "string",
            "description": "The location of the workspace."
        },
        "sku": {
            "type": "string",
            "description": "The SKU name (also referred as edition).",
            "pattern": "basic|enterprise"
        },
        "storage_account": {
            "type": "string",
            "description": "An existing storage account in the Azure resource ID format.",
            "pattern": "Microsoft.Storage\/storageAccounts\/.+"
        },
        "key_vault": {
            "type": "string",
            "description": "An existing key vault in the Azure resource ID format.",
            "pattern": "Microsoft.KeyVault\/vaults\/.+"
        },
        "app_insights": {
            "type": "string",
            "description": "An existing Application Insights in the Azure resource ID format.",
            "pattern": "Microsoft.Insights\/components\/.+"
        },
        "container_registry": {
            "type": "string",
            "description": "An existing container registry in the Azure resource ID format.",
            "pattern": "Microsoft.ContainerRegistry\/registries\/.+"
        },
        "cmk_key_vault": {
            "type": "string",
            "description": "The key vault containing the customer managed key in the Azure resource ID format.",
            "pattern": "Microsoft.KeyVault\/vaults\/.+"
        },
        "resource_cmk_uri": {
            "type": "string",
            "description": "The key URI of the customer managed key to encrypt the data at rest.",
            "pattern": "https:\/\/.+"
        },
        "hbi_workspace": {
            "type": "boolean",
            "description": "Specifies whether the customer data is of High Business Impact(HBI), i.e., contains sensitive business information."
        }
    }
}
