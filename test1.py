#!/usr/bin/env python3

import json
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest

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

# Initialize the Compute, Network, and Resource Graph Clients
compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)
resource_graph_client = ResourceGraphClient(credential)

# Resource Graph query to get all VMs with their attributes
query = QueryRequest(
    subscriptions=[SUBSCRIPTION_ID],
    query="resources | where type == 'microsoft.compute/virtualmachines'"
)

# Execute the query
result = resource_graph_client.resources(query)

# Initialize inventory structure
inventory = {
    "_meta": {
        "hostvars": {}
    },
    "all": {
        "hosts": [],
        "children": []
    }
}

# Process VMs and create inventory
for vm in result.data:
    vm_name = vm['name']
    host_vars = vm  # Start with all attributes from the result

    # Get VM IP address using Compute Management Client
    vm_id = vm['id']
    vm_obj = compute_client.virtual_machines.get(RESOURCE_GROUP, vm_name)
    nic_id = vm_obj.network_profile.network_interfaces[0].id.split('/')[-1]
    nic = network_client.network_interfaces.get(RESOURCE_GROUP, nic_id)
    private_ip = nic.ip_configurations[0].private_ip_address

    # Add IP address to host variables
    host_vars['ansible_host'] = private_ip

    # Add VM to inventory
    inventory["_meta"]["hostvars"][vm_name] = host_vars
    inventory["all"]["hosts"].append(vm_name)

# Print the inventory as JSON for testing
print(json.dumps(inventory, indent=2))
