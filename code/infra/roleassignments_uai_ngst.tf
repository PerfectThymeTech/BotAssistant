resource "azurerm_role_assignment" "uai_ngst_roleassignment_storage_blob_data_owner" {
  description          = "Required for reding and writing data from the function."
  scope                = module.storage_account.storage_account_id
  role_definition_name = "Storage Blob Data Owner"
  principal_id         = module.user_assigned_identity_ingestion.user_assigned_identity_principal_id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_role_assignment" "uai_ngst_roleassignment_open_ai_contributor" {
  description          = "Required for accessing azure open ai from the function."
  scope                = module.azure_open_ai.cognitive_account_id
  role_definition_name = "Cognitive Services OpenAI Contributor"
  principal_id         = module.user_assigned_identity_ingestion.user_assigned_identity_principal_id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_role_assignment" "uai_ngst_roleassignment_key_vault_secrets_officer" {
  description          = "Required for reading and writing secrets in the key vault from the function."
  scope                = module.key_vault_ingestion.key_vault_id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = module.user_assigned_identity_ingestion.user_assigned_identity_principal_id
  principal_type       = "ServicePrincipal"
}
