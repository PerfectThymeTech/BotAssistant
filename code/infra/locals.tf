locals {
  # Naming locals
  prefix = "${lower(var.prefix)}-${var.environment}"

  # Web app locals
  app_settings_default = {
    WEBSITE_VNET_ROUTE_ALL  = "1"
    WEBSITE_CONTENTOVERVNET = "1"
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
}
