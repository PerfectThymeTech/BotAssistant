resource "azurerm_role_assignment" "data_factory_roleassignment_storage_blob_data_owner" {
  description          = "Required for reding and writing data from data factory."
  scope                = module.storage_account.storage_account_id
  role_definition_name = "Storage Blob Data Owner"
  principal_id         = module.data_factory.data_factory_principal_id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_role_assignment" "data_factory_roleassignment_key_vault_secrets_user" {
  description          = "Required for accessing secrets in the key vault from the data factory."
  scope                = module.key_vault_ingestion.key_vault_id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = module.data_factory.data_factory_principal_id
  principal_type       = "ServicePrincipal"
}
