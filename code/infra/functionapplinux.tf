resource "azapi_resource" "linux_function_app" {
  type      = "Microsoft.Web/sites@2024-04-01"
  name      = "${local.prefix}-fctn001"
  location  = var.location
  parent_id = azurerm_resource_group.resource_group_ingestion.id
  tags      = var.tags
  identity {
    type = "UserAssigned"
    identity_ids = [
      module.user_assigned_identity_ingestion.user_assigned_identity_id,
    ]
  }

  body = {
    kind = "functionapp,linux",
    properties = {
      autoGeneratedDomainNameLabelScope = "TenantReuse"
      clientAffinityEnabled             = false
      clientCertEnabled                 = false
      clientCertExclusionPaths          = null
      clientCertMode                    = "Required"
      dailyMemoryTimeQuota              = 0
      daprConfig                        = null
      dnsConfiguration                  = {}
      enabled                           = true
      endToEndEncryptionEnabled         = true
      functionAppConfig = {
        deployment = {
          storage = {
            authentication = {
              type                           = "UserAssignedIdentity"
              userAssignedIdentityResourceId = module.user_assigned_identity_ingestion.user_assigned_identity_id
            }
            type  = "blobContainer"
            value = "${module.storage_account_function.storage_account_primary_blob_endpoint}${local.storage_account_container_function_code_name}"
          }
        }
        runtime = {
          name    = "python"
          version = "3.11"
        }
        scaleAndConcurrency = {
          alwaysReady          = []
          instanceMemoryMB     = 2048
          maximumInstanceCount = 40
          triggers = {
            http = {
              perInstanceConcurrency = 5
            }
          }
        }
      }
      hostNamesDisabled         = false
      hostNameSslStates         = []
      httpsOnly                 = true
      hyperV                    = false
      ipMode                    = "IPv4"
      keyVaultReferenceIdentity = module.user_assigned_identity_ingestion.user_assigned_identity_id
      publicNetworkAccess       = "Enabled"
      redundancyMode            = null
      scmSiteAlsoStopped        = false
      serverFarmId              = module.app_service_plan_ingestion.service_plan_id
      storageAccountRequired    = true
      virtualNetworkSubnetId    = azapi_resource.subnet_function.id
      siteConfig = {
        appSettings = [
          {
            name  = "AzureWebJobsStorage__accountName"
            value = module.storage_account_function.storage_account_name
          },
          {
            name  = "AzureWebJobsStorage__credential"
            value = "managedidentity"
          },
          {
            name  = "AzureWebJobsStorage__clientId"
            value = module.user_assigned_identity_ingestion.user_assigned_identity_client_id
          },
          {
            name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
            value = module.application_insights.application_insights_connection_string
          },
          {
            name  = "MANAGED_IDENTITY_CLIENT_ID"
            value = module.user_assigned_identity_ingestion.user_assigned_identity_client_id
          },
          {
            name  = "AzureWebJobsSecretStorageType"
            value = "keyvault"
          },
          {
            name  = "AzureWebJobsSecretStorageKeyVaultUri"
            value = module.key_vault_ingestion.key_vault_uri
          },
          {
            name  = "AzureWebJobsSecretStorageKeyVaultClientId"
            value = module.user_assigned_identity_ingestion.user_assigned_identity_client_id
          },
          {
            name  = "AZURE_FUNCTIONS_ENVIRONMENT"
            value = "Production"
          },
        ]
        # autoSwapSlotName = ""
        detailedErrorLoggingEnabled            = true
        functionsRuntimeScaleMonitoringEnabled = null # Not available for flex plans
        healthCheckPath                        = null
        http20Enabled                          = true
        httpLoggingEnabled                     = true
        ipSecurityRestrictions                 = []
        ipSecurityRestrictionsDefaultAction    = "Allow" # "Deny"
        keyVaultReferenceIdentity              = module.user_assigned_identity_consumption.user_assigned_identity_id
        loadBalancing                          = "LeastRequests"
        localMySqlEnabled                      = false
        # minTlsCipherSuite = ""
        minTlsVersion                          = "1.3"
        publicNetworkAccess                    = "Enabled"
        remoteDebuggingEnabled                 = false
        requestTracingEnabled                  = true
        scmIpSecurityRestrictions              = []
        scmIpSecurityRestrictionsDefaultAction = "Allow" # "Deny"
        scmIpSecurityRestrictionsUseMain       = false
        scmMinTlsVersion                       = "1.3"
        scmType                                = "None"
        websiteTimeZone                        = "UTC"
        webSocketsEnabled                      = false

      }
    }
  }

  response_export_values    = ["*"]
  schema_validation_enabled = true
  locks                     = []
  ignore_casing             = false
  ignore_missing_property   = false
}

data "azurerm_monitor_diagnostic_categories" "diagnostic_categories_linux_function_app" {
  resource_id = azapi_resource.linux_function_app.id
}

resource "azurerm_monitor_diagnostic_setting" "diagnostic_setting_linux_function_app" {
  name                       = "logAnalytics"
  target_resource_id         = azapi_resource.linux_function_app.id
  log_analytics_workspace_id = data.azurerm_log_analytics_workspace.log_analytics_workspace.id

  dynamic "enabled_log" {
    iterator = entry
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_linux_function_app.log_category_groups
    content {
      category_group = entry.value
    }
  }

  dynamic "metric" {
    iterator = entry
    for_each = data.azurerm_monitor_diagnostic_categories.diagnostic_categories_linux_function_app.metrics
    content {
      category = entry.value
      enabled  = true
    }
  }
}

resource "azurerm_private_endpoint" "linux_function_app_private_endpoint" {
  name                = "${azapi_resource.linux_function_app.name}-pe"
  location            = var.location
  resource_group_name = azurerm_resource_group.resource_group_ingestion.name
  tags                = var.tags

  custom_network_interface_name = "${azapi_resource.linux_function_app.name}-nic"
  private_service_connection {
    name                           = "${azapi_resource.linux_function_app.name}-pe"
    is_manual_connection           = false
    private_connection_resource_id = azapi_resource.linux_function_app.id
    subresource_names              = ["sites"]
  }
  subnet_id = azapi_resource.subnet_private_endpoints.id
  dynamic "private_dns_zone_group" {
    for_each = var.private_dns_zone_id_sites == "" ? [] : [1]
    content {
      name = "${azapi_resource.linux_function_app.name}-arecord"
      private_dns_zone_ids = [
        var.private_dns_zone_id_sites
      ]
    }
  }

  lifecycle {
    ignore_changes = [
      private_dns_zone_group
    ]
  }
}
