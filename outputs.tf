output "vm_public_ip" {
  description = "IP público da VM Linux para acesso SSH"
  value       = azurerm_public_ip.pip_vm.ip_address
}

output "vm_private_ip" {
  description = "IP privado da VM Linux (alvo do Prometheus)"
  value       = azurerm_network_interface.nic_vm.private_ip_address
}

output "aci_private_ip" {
  description = "IP privado do grupo de containers (Prometheus + Grafana)"
  value       = azurerm_container_group.aci.ip_address
}

output "grafana_tunnel_command" {
  description = "Comando para abrir o túnel SSH e acessar o Grafana em http://localhost:3000"
  value       = "ssh -L 3000:${azurerm_container_group.aci.ip_address}:3000 ${var.admin_username}@${azurerm_public_ip.pip_vm.ip_address}"
}