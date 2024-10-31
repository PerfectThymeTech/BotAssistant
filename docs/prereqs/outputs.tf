output "virtual_network_id" {
  description = "Specifies the id of the virtual network."
  sensitive   = true
  value       = azurerm_virtual_network.virtual_network.id
}

output "route_table_id" {
  description = "Specifies the id of the route table."
  sensitive   = true
  value       = azurerm_route_table.route_table.id
}

output "network_security_group_id" {
  description = "Specifies the id of the network security group."
  sensitive   = true
  value       = azurerm_network_security_group.network_security_group.id
}

output "log_analytics_workspace_id" {
  description = "Specifies the id of the log analytics workspace."
  sensitive   = true
  value       = module.log_analytics_workspace.log_analytics_workspace_id
}

output "application_client_id" {
  description = "Specifies the application client id."
  sensitive   = true
  value       = azuread_application.application.client_id
}

output "application_password" {
  description = "Specifies the application client secret."
  sensitive   = true
  value       = tolist(azuread_application.application.password).0.value
}

output "application_tenant_id" {
  description = "Specifies the application tenant id."
  sensitive   = true
  value       = data.azuread_client_config.current.tenant_id
}
