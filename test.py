import json
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

# Initialize the Compute Management Client
compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)

# Fetch the list of VMs in the specified resource group
vms = compute_client.virtual_machines.list(RESOURCE_GROUP)

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
for vm in vms:
    vm_name = vm.name
    tags = vm.tags

    # Skip VMs without required tags
    if not tags or "role" not in tags or "env_group" not in tags or "environment" not in tags:
        continue

    # Get VM IP address
    nic_id = vm.network_profile.network_interfaces[0].id.split('/')[-1]
    nic = network_client.network_interfaces.get(RESOURCE_GROUP, nic_id)
    private_ip = nic.ip_configurations[0].private_ip_address

    # Add VM to inventory
    inventory["_meta"]["hostvars"][vm_name] = {
        "ansible_host": private_ip,
        "role": tags["role"],
        "env_group": tags["env_group"],
        "environment": tags["environment"]
    }
    inventory["all"]["hosts"].append(vm_name)

# Print the inventory as JSON for testing
print(json.dumps(inventory, indent=2))
