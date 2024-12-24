resource "azurerm_role_assignment" "uai_cnsm_roleassignment_open_ai_contributor" {
  description          = "Required for accessing azure open ai from the web app."
  scope                = module.azure_open_ai.cognitive_account_id
  role_definition_name = "Cognitive Services OpenAI Contributor"
  principal_id         = module.user_assigned_identity_consumption.user_assigned_identity_principal_id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_role_assignment" "uai_cnsm_roleassignment_key_vault_secrets_user" {
  description          = "Required for accessing secrets in the key vault from teh web app app settings."
  scope                = module.key_vault_consumption.key_vault_id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = module.user_assigned_identity_consumption.user_assigned_identity_principal_id
  principal_type       = "ServicePrincipal"
}
