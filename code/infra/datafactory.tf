module "data_factory" {
  source = "github.com/PerfectThymeTech/terraform-azurerm-modules//modules/datafactory?ref=main"
  providers = {
    azurerm = azurerm
    azapi   = azapi
    time    = time
  }

  location                                          = var.location
  resource_group_name                               = azurerm_resource_group.resource_group_ingestion.name
  tags                                              = var.tags
  data_factory_name                                 = "${local.prefix}-adf001"
  data_factory_purview_id                           = null
  data_factory_azure_devops_repo                    = {}
  data_factory_github_repo                          = {}
  data_factory_global_parameters                    = {}
  data_factory_published_content                    = {}
  data_factory_published_content_template_variables = {}
  data_factory_triggers_start                       = []
  data_factory_pipelines_run                        = []
  data_factory_managed_private_endpoints = {
    "storage-blob" = {
      subresource_name   = "blob"
      target_resource_id = module.storage_account.storage_account_id
    }
    "keyvault-vault" = {
      subresource_name   = "vault"
      target_resource_id = module.key_vault_ingestion.key_vault_id
    }
  }
  diagnostics_configurations       = local.diagnostics_configurations
  subnet_id                        = azapi_resource.subnet_private_endpoints.id
  connectivity_delay_in_seconds    = var.connectivity_delay_in_seconds
  private_dns_zone_id_data_factory = var.private_dns_zone_id_data_factory
  customer_managed_key             = local.customer_managed_key
}
