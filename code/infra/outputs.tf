output "bot_service_name" {
  description = "Specifies the resource id of the bot service."
  value       = reverse(split(module.bot_service.bot_service_id, "/"))[0]
  sensitive   = false
}

output "bot_service_id" {
  description = "Specifies the resource id of the bot service."
  value       = module.bot_service.bot_service_id
  sensitive   = false
}
