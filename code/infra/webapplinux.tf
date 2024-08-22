resource "azurerm_linux_web_app" "linux_web_app" {
  name                = "${local.prefix}-app001"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
  identity {
    type = "UserAssigned"
    identity_ids = [
      module.user_assigned_identity.user_assigned_identity_id
    ]
  }

  app_settings = local.app_settings
  client_affinity_enabled = false
  client_certificate_enabled = false
  client_certificate_exclusion_paths = null
  client_certificate_mode = "Optional"
  enabled = true
  ftp_publish_basic_authentication_enabled = false
  https_only = true
  key_vault_reference_identity_id = module.user_assigned_identity.user_assigned_identity_id
  public_network_access_enabled = true
  service_plan_id = module.app_service_plan.service_plan_id
  site_config {
    always_on = true
    api_definition_url = null
    api_management_api_id = null
    app_command_line = null
    application_stack {
      python_version = "3.11"
    }
    auto_heal_enabled = false
    container_registry_managed_identity_client_id = null
    container_registry_use_managed_identity = null
    ftps_state = "Disabled"
    http2_enabled = true
    ip_restriction_default_action = "Deny"
    load_balancing_mode = "LeastRequests"
    local_mysql_enabled = false
    managed_pipeline_mode = "Integrated"
    minimum_tls_version = "1.2"
    remote_debugging_enabled = false
    remote_debugging_version = null
    scm_ip_restriction_default_action = "Deny"
    scm_use_main_ip_restriction = false
    scm_minimum_tls_version = "1.2"
    use_32_bit_worker = false
    vnet_route_all_enabled = true
    websockets_enabled = false
    worker_count = 1

    # auto_heal_setting {
    #   action {
    #     action_type = 
    #   }
    #   trigger {
        
    #   }
    # }
  }
  virtual_network_subnet_id = var.web_app_subnet_id
  webdeploy_publish_basic_authentication_enabled = false
}
