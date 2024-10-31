module "log_analytics_workspace" {
  source = "github.com/PerfectThymeTech/terraform-azurerm-modules//modules/loganalytics?ref=main"
  providers = {
    azurerm = azurerm
  }

  location                                  = var.location
  resource_group_name                       = azurerm_resource_group.resource_group.name
  tags                                      = var.tags
  log_analytics_workspace_name              = "${local.prefix}-law001"
  log_analytics_workspace_retention_in_days = 30
  diagnostics_configurations                = []
}
