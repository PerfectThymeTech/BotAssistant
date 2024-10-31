resource "azurerm_resource_group" "resource_group" {
  name     = "${local.prefix}-prereq-rg"
  location = var.location
  tags     = var.tags
}
