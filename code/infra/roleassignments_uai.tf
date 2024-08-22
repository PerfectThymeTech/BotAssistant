resource "azurerm_role_assignment" "uai_roleassignment_open_ai_user" {
  description          = "Required for accessing azure open ai from the web app"
  scope                = module.azure_open_ai.cognitive_account_id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = module.user_assigned_identity.user_assigned_identity_principal_id
  principal_type       = "ServicePrincipal"
}
