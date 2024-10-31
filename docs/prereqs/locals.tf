locals {
  # Naming locals
  prefix = "${lower(var.prefix)}-${var.environment}"
  resource_providers_to_register = [
    "Microsoft.Authorization",
    "Microsoft.OperationalInsights",
    "microsoft.insights",
    "Microsoft.Network",
    "Microsoft.Resources",
  ]

  # AAD App locals
  application_name = "bot-oauth"
  redirect_uris = {
    none   = "https://token.botframework.com/.auth/web/redirect"
    europe = "https://europe.token.botframework.com/.auth/web/redirect"
    us     = "https://unitedstates.token.botframework.com/.auth/web/redirect"
    india  = "https://india.token.botframework.com/.auth/web/redirect"
    gov    = "https://token.botframework.azure.us/.auth/web/redirect"
  }

  # DNS variables
  private_dns_zone_names = [
    "privatelink.vaultcore.azure.net",
    "privatelink.azurewebsites.net",
    "privatelink.directline.botframework.com",
    "privatelink.token.botframework.com",
    "privatelink.openai.azure.com",
    "privatelink.documents.azure.com",
  ]
}