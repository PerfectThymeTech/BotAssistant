module "bot_service" {
  source = "github.com/PerfectThymeTech/terraform-azurerm-modules//modules/botservice?ref=main"
  providers = {
    azurerm = azurerm
    time    = time
  }

  location             = var.location
  resource_group_name  = azurerm_resource_group.resource_group.name
  tags                 = var.tags
  bot_service_name     = "${local.prefix}-bot001"
  bot_service_location = "global"
  bot_service_endpoint = "https://${azurerm_linux_web_app.linux_web_app.default_hostname}/api/messages"
  bot_service_luis = {
    app_ids = []
    key     = null
  }
  bot_service_microsoft_app = {
    app_id        = module.user_assigned_identity.user_assigned_identity_client_id
    app_msi_id    = module.user_assigned_identity.user_assigned_identity_id
    app_tenant_id = module.user_assigned_identity.user_assigned_identity_tenant_id
    app_type      = "UserAssignedMSI"
  }
  bot_service_sku                              = "S1"
  bot_service_streaming_endpoint_enabled       = false
  bot_service_public_network_access_enabled    = true
  bot_service_application_insights_id          = module.application_insights.application_insights_id
  diagnostics_configurations                   = local.diagnostics_configurations
  subnet_id                                    = azapi_resource.subnet_private_endpoints.id
  connectivity_delay_in_seconds                = var.connectivity_delay_in_seconds
  private_dns_zone_id_bot_framework_directline = var.private_dns_zone_id_bot_framework_directline
  private_dns_zone_id_bot_framework_token      = var.private_dns_zone_id_bot_framework_token
  customer_managed_key                         = local.customer_managed_key
}

resource "azurerm_bot_connection" "bot_connection_aad" {
  name                = "aad"
  bot_name            = reverse(split(module.bot_service.bot_service_id, "/"))[0]
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name

  client_id     = var.bot_oauth_client_id
  client_secret = var.bot_oauth_client_secret
  parameters = {
    "TenantId" = data.azurerm_client_config.current.tenant_id
  }
  service_provider_name = "Azure Active Directory v2" # serviceProviderId = "30dd229c-58e3-4a48-bdfd-91ec48eb906c"
  scopes                = join(" ", var.bot_oauth_scopes)
}
