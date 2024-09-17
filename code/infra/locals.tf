locals {
  # Naming locals
  prefix = "${lower(var.prefix)}-${var.environment}"

  # Web app locals
  app_settings_default = {
    # Configuration app settings
    APPLICATIONINSIGHTS_CONNECTION_STRING      = module.application_insights.application_insights_connection_string
    ApplicationInsightsAgent_EXTENSION_VERSION = "~3"
    SCM_DO_BUILD_DURING_DEPLOYMENT             = "1"
    WEBSITE_CONTENTOVERVNET                    = "1"

    # Auth app settings
    MICROSOFT_APP_ID           = module.user_assigned_identity.user_assigned_identity_client_id
    MICROSOFT_APP_PASSWORD     = ""
    MICROSOFT_APP_TENANTID     = module.user_assigned_identity.user_assigned_identity_tenant_id
    MICROSOFT_APP_TYPE         = "UserAssignedMSI"
    MANAGED_IDENTITY_CLIENT_ID = module.user_assigned_identity.user_assigned_identity_client_id
    OAUTH_CONNECTION_NAME      = azurerm_bot_connection.bot_connection_aadv2_oauth.name

    # Azure open ai app settings
    AZURE_OPEN_AI_ENDPOINT     = module.azure_open_ai.cognitive_account_endpoint
    AZURE_OPEN_AI_API_VERSION  = "2024-05-01-preview"
    AZURE_OPENAI_MODEL_NAME    = azurerm_cognitive_deployment.cognitive_deployment_gpt_4o.name
    AZURE_OPENAI_SYSTEM_PROMPT = data.local_file.file_system_prompt.content
    AZURE_OPENAI_ASSISTANT_ID  = ""

    # Cosmos DB settings
    AZURE_COSMOS_ENDPOINT     = module.cosmosdb_account.cosmosdb_account_endpoint
    AZURE_COSMOS_KEY          = module.cosmosdb_account.cosmosdb_account_primary_key
    AZURE_COSMOS_DATABASE_ID  = azurerm_cosmosdb_sql_database.cosmosdb_sql_database.name
    AZURE_COSMOS_CONTAINER_ID = azurerm_cosmosdb_sql_container.cosmosdb_sql_container.name
  }
  web_app_app_settings = merge(local.app_settings_default, var.web_app_app_settings)

  # Resource locals
  virtual_network = {
    resource_group_name = split("/", var.vnet_id)[4]
    name                = split("/", var.vnet_id)[8]
  }
  network_security_group = {
    resource_group_name = split("/", var.nsg_id)[4]
    name                = split("/", var.nsg_id)[8]
  }
  route_table = {
    resource_group_name = split("/", var.route_table_id)[4]
    name                = split("/", var.route_table_id)[8]
  }
  log_analytics_workspace = {
    resource_group_name = split("/", var.log_analytics_workspace_id)[4]
    name                = split("/", var.log_analytics_workspace_id)[8]
  }

  # Logging locals
  diagnostics_configurations = [
    {
      log_analytics_workspace_id = var.log_analytics_workspace_id
      storage_account_id         = ""
    }
  ]

  # CMK locals
  customer_managed_key = null

  # Other locals
  system_prompt_code_path     = "${path.module}/../../docs/SystemPrompt.txt"
  cosmosdb_sql_container_name = "user-state"
}
