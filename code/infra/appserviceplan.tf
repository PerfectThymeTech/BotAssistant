module "app_service_plan" {
  source = "github.com/PerfectThymeTech/terraform-azurerm-modules//modules/appserviceplan?ref=main"
  providers = {
    azurerm = azurerm
    time    = time
  }

  location                                  = var.location
  resource_group_name                       = var.resource_group_name
  tags                                      = var.tags
  service_plan_name                         = "${local.prefix}-asp001"
  service_plan_maximum_elastic_worker_count = null
  service_plan_os_type                      = "Linux"
  service_plan_per_site_scaling_enabled     = false
  service_plan_sku_name                     = "B1"
  service_plan_worker_count                 = 1
  service_plan_zone_balancing_enabled       = false
  diagnostics_configurations                = var.diagnostics_configurations
}
