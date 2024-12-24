resource "azurerm_resource_group" "resource_group_consumption" {
  name     = "${local.prefix}-bot-cnsm-rg"
  location = var.location
  tags     = var.tags
}

resource "azurerm_resource_group" "resource_group_ingestion" {
  name     = "${local.prefix}-bot-ngst-rg"
  location = var.location
  tags     = var.tags
}

resource "azurerm_resource_group" "resource_group_monitoring" {
  name     = "${local.prefix}-bot-mntrng-rg"
  location = var.location
  tags     = var.tags
}
