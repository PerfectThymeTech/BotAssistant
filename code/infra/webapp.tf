resource "azurerm_windows_web_app" "windows_web_app" {
  name                = "${local.prefix}-asp001"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name
  tags                = var.tags
  identity {
    type = "SystemAssigned, UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.user_assigned_identity.id
    ]
  }

  app_settings = {
    # "NODE_NAME"  = azurerm_data_factory_integration_runtime_self_hosted.data_factory_integration_runtime_self_hosted.name # Use default hostname value instead of manual value
    "ENABLE_HA"                           = "false"
    "HA_PORT"                             = "8060"
    "ENABLE_AE"                           = "false"
    "AE_TIME"                             = "600"
    "AUTH_KEY"                            = azurerm_data_factory_integration_runtime_self_hosted.data_factory_integration_runtime_self_hosted.primary_authorization_key # "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.key_vault_secret_shir_key.versionless_id})"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "WEBSITE_CONTENTOVERVNET"             = "1"
    "WEBSITE_DNS_SERVER"                  = var.dns_server_ip
  }
  client_affinity_enabled                  = false
  client_certificate_enabled               = false
  client_certificate_exclusion_paths       = ""
  client_certificate_mode                  = "Required"
  enabled                                  = true
  ftp_publish_basic_authentication_enabled = false
  https_only                               = true
  key_vault_reference_identity_id          = azurerm_user_assigned_identity.user_assigned_identity.id
  public_network_access_enabled            = false
  # storage_account { # TODO
  # }
  virtual_network_subnet_id                      = azapi_resource.subnet_container.id
  webdeploy_publish_basic_authentication_enabled = false
  site_config {
    always_on = true
    application_stack {
      docker_image_name   = local.container_registry_image
      docker_registry_url = "https://${local.container_registry_url}"
      # docker_registry_username = ""
      # docker_registry_password = ""
    }
    container_registry_managed_identity_client_id = azurerm_user_assigned_identity.user_assigned_identity.client_id
    container_registry_use_managed_identity       = true
    ftps_state                                    = "Disabled"
    http2_enabled                                 = true
    load_balancing_mode                           = "LeastRequests"
    local_mysql_enabled                           = false
    managed_pipeline_mode                         = "Integrated"
    minimum_tls_version                           = "1.2"
    scm_minimum_tls_version                       = "1.2"
    scm_use_main_ip_restriction                   = false
    remote_debugging_enabled                      = false
    remote_debugging_version                      = "VS2022"
    use_32_bit_worker                             = null
    vnet_route_all_enabled                        = true
    websockets_enabled                            = false
    worker_count                                  = null
  }
  service_plan_id = azurerm_service_plan.service_plan.id
}

data "azurerm_monitor_diagnostic_categories" "diagnostic_categories_windows_web_app" {
  resource_id = azurerm_windows_web_app.windows_web_app.id
}

resource "azurerm_monitor_diagnostic_setting" "diagnostic_setting_windows_web_app" {
  name                       = "logAnalytics"
  target_resource_id         = azurerm_windows_web_app.windows_web_app.id
  log_analytics_workspace_id = data.azurerm_log_analytics_workspace.log_analytics_workspace.id

  dynamic "enabled_log" {
    iterator = entry
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_windows_web_app.log_category_groups
    content {
      category_group = entry.value
    }
  }

  dynamic "metric" {
    iterator = entry
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_windows_web_app.metrics
    content {
      category = entry.value
      enabled  = true
    }
  }
}

resource "azurerm_private_endpoint" "windows_web_app_private_endpoint" {
  name                = "${azurerm_windows_web_app.windows_web_app.name}-pe"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group.name
  tags                = var.tags

  custom_network_interface_name = "${azurerm_windows_web_app.windows_web_app.name}-nic"
  private_service_connection {
    name                           = "${azurerm_windows_web_app.windows_web_app.name}-pe"
    is_manual_connection           = false
    private_connection_resource_id = azurerm_windows_web_app.windows_web_app.id
    subresource_names              = ["sites"]
  }
  subnet_id = azapi_resource.subnet_private_endpoints.id
  private_dns_zone_group {
    name = "${azurerm_windows_web_app.windows_web_app.name}-arecord"
    private_dns_zone_ids = [
      var.private_dns_zone_id_sites
    ]
  }
}
