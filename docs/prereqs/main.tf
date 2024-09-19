variable "data_residency" {
  description = "Specifies the data residency requirements of the bot framework."
  type        = string
  sensitive   = false
  nullable    = false
  default     = "none"
  validation {
    condition     = contains(["none", "europe", "us", "india", "gov"], var.data_residency)
    error_message = "Please specify a valid data residency. Must be one of 'none', 'europe', 'us', 'india', or 'gov'."
  }
}

# Terraform
terraform {
  required_version = ">=0.12"

  required_providers {
    azuread = {
      source  = "hashicorp/azuread"
      version = "2.53.1"
    }
    time = {
      source  = "hashicorp/time"
      version = "0.12.1"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.6.3"
    }
  }
}

# Providers

# Locals
locals {
  application_name = "bot-oauth"

  redirect_uris = {
    none   = "https://token.botframework.com/.auth/web/redirect"
    europe = "https://europe.token.botframework.com/.auth/web/redirect"
    us     = "https://unitedstates.token.botframework.com/.auth/web/redirect"
    india  = "https://india.token.botframework.com/.auth/web/redirect"
    gov    = "https://token.botframework.azure.us/.auth/web/redirect"
  }
}

# Data
data "azuread_client_config" "current" {}

# Resources
resource "time_rotating" "expiration" {
  rotation_days = 180
}

resource "random_uuid" "uuid_application_app_role" {}

resource "azuread_application" "application" {
  display_name = local.application_name
  description  = "Azure AD OAuth Bot App"

  notes                         = "Some Notes"
  oauth2_post_response_required = false
  owners                        = [data.azuread_client_config.current.object_id]
  prevent_duplicate_names       = true
  sign_in_audience              = "AzureADMyOrg"

  password {
    display_name = "bot-login"
    start_date   = time_rotating.expiration.id
    end_date     = timeadd(time_rotating.expiration.id, "4320h")
  }
  required_resource_access {
    resource_app_id = "00000003-0000-0000-c000-000000000000" # Microsoft Graph
    resource_access {
      id   = "37f7f235-527c-4136-accd-4a02d197296e" # openid
      type = "Scope"
    }
    resource_access {
      id   = "14dad69e-099b-42c9-810b-d002981feec1" # profile
      type = "Scope"
    }
    resource_access {
      id   = "e1fe6dd8-ba31-4d61-89e7-88639da4683d" # User.Read
      type = "Scope"
    }
    resource_access {
      id   = "b340eb25-3456-403f-be2f-af7a0d370277" # User.ReadBasic.All
      type = "Scope"
    }
  }
  web {
    redirect_uris = [
      local.redirect_uris[var.data_residency],
      # "https://login.microsoftonline.com",
    ]
  }
}

# Outputs
output "application_client_id" {
  sensitive = true
  value     = azuread_application.application.client_id
}

output "application_password" {
  sensitive = true
  value     = tolist(azuread_application.application.password).0.value
}

output "application_tenant_id" {
  sensitive = true
  value     = data.azuread_client_config.current.tenant_id
}
