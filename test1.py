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

# Print the query result for inspection
print(json.dumps(result.data, indent=2))
