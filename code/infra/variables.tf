# General variables
variable "location" {
  description = "Specifies the location for all Azure resources."
  type        = string
  sensitive   = false
}

variable "environment" {
  description = "Specifies the environment of the deployment."
  type        = string
  sensitive   = false
  default     = "dev"
  validation {
    condition     = contains(["int", "dev", "tst", "qa", "uat", "prd"], var.environment)
    error_message = "Please use an allowed value: \"int\", \"dev\", \"tst\", \"qa\", \"uat\" or \"prd\"."
  }
}

variable "prefix" {
  description = "Specifies the prefix for all resources created in this deployment."
  type        = string
  sensitive   = false
  validation {
    condition     = length(var.prefix) >= 2 && length(var.prefix) <= 10
    error_message = "Please specify a prefix with more than two and less than 10 characters."
  }
}

variable "tags" {
  description = "Specifies the tags that you want to apply to all resources."
  type        = map(string)
  sensitive   = false
  default     = {}
}

# Service variables
variable "web_app_app_settings" {
  description = "Specifies the videoindexer id"
  type        = map(string)
  sensitive   = false
}

# Logging variables
variable "log_analytics_workspace_id" {
  description = "Specifies the resource ID of the log analytics workspace used for collecting logs."
  type        = string
  sensitive   = false
  validation {
    condition     = length(split("/", var.log_analytics_workspace_id)) == 9
    error_message = "Please specify a valid resource ID."
  }
}

# Network variables
variable "vnet_id" {
  description = "Specifies the resource ID of the Vnet used for the Azure Function."
  type        = string
  sensitive   = false
  validation {
    condition     = length(split("/", var.vnet_id)) == 9
    error_message = "Please specify a valid resource ID."
  }
}

variable "nsg_id" {
  description = "Specifies the resource ID of the default network security group for the Azure Function."
  type        = string
  sensitive   = false
  validation {
    condition     = length(split("/", var.nsg_id)) == 9
    error_message = "Please specify a valid resource ID."
  }
}

variable "route_table_id" {
  description = "Specifies the resource ID of the default route table for the Azure Function."
  type        = string
  sensitive   = false
  validation {
    condition     = length(split("/", var.route_table_id)) == 9
    error_message = "Please specify a valid resource ID."
  }
}

variable "subnet_cidr_web_app" {
  description = "Specifies the subnet cidr range for the web app subnet."
  type        = string
  sensitive   = false
  validation {
    condition     = length(split("/", var.subnet_cidr_web_app)) == 2
    error_message = "Please specify a valid subnet cidr range."
  }
}

variable "subnet_cidr_private_endpoints" {
  description = "Specifies the subnet cidr range for private endpoints."
  type        = string
  sensitive   = false
  validation {
    condition     = length(split("/", var.subnet_cidr_private_endpoints)) == 2
    error_message = "Please specify a valid subnet cidr range."
  }
}

variable "private_dns_zone_id_key_vault" {
  description = "Specifies the resource ID of the private DNS zone for Azure Key Vault. Not required if DNS A-records get created via Azure Policy."
  type        = string
  sensitive   = false
  default     = ""
  validation {
    condition     = var.private_dns_zone_id_key_vault == "" || (length(split("/", var.private_dns_zone_id_key_vault)) == 9 && endswith(var.private_dns_zone_id_key_vault, "privatelink.vaultcore.azure.net"))
    error_message = "Please specify a valid resource ID for the private DNS Zone."
  }
}

variable "private_dns_zone_id_sites" {
  description = "Specifies the resource ID of the private DNS zone for Azure Websites. Not required if DNS A-records get created via Azue Policy."
  type        = string
  sensitive   = false
  default     = ""
  validation {
    condition     = var.private_dns_zone_id_sites == "" || (length(split("/", var.private_dns_zone_id_sites)) == 9 && endswith(var.private_dns_zone_id_sites, "privatelink.azurewebsites.net"))
    error_message = "Please specify a valid resource ID for the private DNS Zone."
  }
}

variable "private_dns_zone_id_bot_framework_directline" {
  description = "Specifies the resource ID of the private DNS zone for the bot framework directline. Not required if DNS A-records get created via Azure Policy."
  type        = string
  sensitive   = false
  default     = ""
  validation {
    condition     = var.private_dns_zone_id_bot_framework_directline == "" || (length(split("/", var.private_dns_zone_id_bot_framework_directline)) == 9 && endswith(var.private_dns_zone_id_bot_framework_directline, "privatelink.directline.botframework.com"))
    error_message = "Please specify a valid resource ID for the private DNS Zone."
  }
}

variable "private_dns_zone_id_bot_framework_token" {
  description = "Specifies the resource ID of the private DNS zone for the bot framework token. Not required if DNS A-records get created via Azure Policy."
  type        = string
  sensitive   = false
  default     = ""
  validation {
    condition     = var.private_dns_zone_id_bot_framework_token == "" || (length(split("/", var.private_dns_zone_id_bot_framework_token)) == 9 && endswith(var.private_dns_zone_id_bot_framework_token, "privatelink.token.botframework.com"))
    error_message = "Please specify a valid resource ID for the private DNS Zone."
  }
}
