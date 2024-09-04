# General variables
location        = "northeurope"
location_openai = "swedencentral"
environment     = "dev"
prefix          = "assis"
tags = {
  workload = "assis"
}

# Service variables
web_app_app_settings = {}

# Logging variables
log_analytics_workspace_id = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/DefaultResourceGroup-NEU/providers/Microsoft.OperationalInsights/workspaces/DefaultWorkspace-8f171ff9-2b5b-4f0f-aed5-7fa360a1d094-NEU"

# Network variables
vnet_id                                      = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-dpml-network-rg/providers/Microsoft.Network/virtualNetworks/mycrp-prd-dpml-vnet001"
nsg_id                                       = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-dpml-network-rg/providers/Microsoft.Network/networkSecurityGroups/mycrp-prd-dpml-nsg001"
route_table_id                               = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-dpml-network-rg/providers/Microsoft.Network/routeTables/mycrp-prd-dpml-rt001"
subnet_cidr_web_app                          = "10.0.96.64/26"
subnet_cidr_private_endpoints                = "10.0.96.128/27"
private_dns_zone_id_vault                    = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net"
private_dns_zone_id_sites                    = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.azurewebsites.net"
private_dns_zone_id_bot_framework_directline = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.directline.botframework.com"
private_dns_zone_id_bot_framework_token      = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.token.botframework.com"
private_dns_zone_id_open_ai                  = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.openai.azure.com"
private_dns_zone_id_cosmos_sql               = "/subscriptions/8f171ff9-2b5b-4f0f-aed5-7fa360a1d094/resourceGroups/mycrp-prd-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.documents.cosmos.azure.com"
