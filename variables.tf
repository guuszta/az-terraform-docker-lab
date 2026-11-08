variable "location" {
  type        = string
  default     = "eastus"
  description = "Região da Azure onde os recursos serão criados."
}

variable "prefix" {
  type        = string
  default     = "aztd-lab"
  description = "Prefixo padronizado para nomear os recursos do laboratório."
}

variable "admin_username" {
  type        = string
  default     = "azureuser"
  description = "Usuário administrador da VM Linux."
}
