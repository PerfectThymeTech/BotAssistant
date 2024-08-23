module "azure_open_ai" {
  source = "github.com/PerfectThymeTech/terraform-azurerm-modules//modules/aiservice?ref=main"
  providers = {
    azurerm = azurerm
    time    = time
  }

  location                                                = var.location_openai
  location_private_endpoint                               = var.location
  resource_group_name                                     = azurerm_resource_group.resource_group.name
  tags                                                    = var.tags
  cognitive_account_name                                  = "${local.prefix}-aoai001"
  cognitive_account_kind                                  = "OpenAI"
  cognitive_account_sku                                   = "S0"
  cognitive_account_firewall_bypass_azure_services        = false
  cognitive_account_outbound_network_access_restricted    = true
  cognitive_account_outbound_network_access_allowed_fqdns = []
  cognitive_account_deployments                           = {}
  # {
  #   gpt-4o = {
  #     model_name     = "gpt-4o"
  #     model_version  = "2024-05-13"
  #     scale_type     = null
  #     scale_tier     = null
  #     scale_size     = null
  #     scale_family   = null
  #     scale_capacity = 100
  #   }
  # }
  diagnostics_configurations            = []
  subnet_id                             = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/tfmdltst-dev-rg/providers/Microsoft.Network/virtualNetworks/tfmdltst-dev-vnet/subnets/PrivateEndpoints"
  connectivity_delay_in_seconds         = 0
  private_dns_zone_id_cognitive_account = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.cognitiveservices.azure.com"
  customer_managed_key                  = null
}

resource "azurerm_cognitive_deployment" "cognitive_deployment_gpt_4o" {
  name                 = "gpt-4o"
  cognitive_account_id = module.azure_open_ai.cognitive_account_id

  model {
    format  = "OpenAI"
    name    = "gpt-4o"
    version = "2024-05-13"
  }
  scale {
    capacity = 100
    type     = "Standard"
  }
}
