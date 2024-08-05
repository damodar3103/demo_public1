#!/usr/bin/env python3

from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient

# Hard-coded Azure credentials and resource group details
AZURE_CLIENT_ID = "<your_client_id>"
AZURE_CLIENT_SECRET = "<your_client_secret>"
AZURE_TENANT_ID = "<your_tenant_id>"
SUBSCRIPTION_ID = "<your_subscription_id>"
RESOURCE_GROUP = "<your_resource_group>"

# Authenticate using ClientSecretCredential
credential = ClientSecretCredential(
    client_id=AZURE_CLIENT_ID,
    client_secret=AZURE_CLIENT_SECRET,
    tenant_id=AZURE_TENANT_ID
)

# Initialize the Compute and Network Management Clients
compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)

# Get a list of VMs in the specified resource group
vms = compute_client.virtual_machines.list(RESOURCE_GROUP)

# Iterate over the VMs and print their public IP addresses
for vm in vms:
    vm_name = vm.name
    nic_id = vm.network_profile.network_interfaces[0].id.split('/')[-1]
    nic = network_client.network_interfaces.get(RESOURCE_GROUP, nic_id)
    
    try:
        # Fetch public IP if available
        public_ip_id = nic.ip_configurations[0].public_ip_address.id.split('/')[-1]
        public_ip = network_client.public_ip_addresses.get(RESOURCE_GROUP, public_ip_id).ip_address
        print(f"VM: {vm_name}, Public IP: {public_ip}")
    except Exception as e:
        print(f"VM: {vm_name}, Public IP: Not available")
