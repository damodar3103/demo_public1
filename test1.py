#!/usr/bin/env python3

from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resourcegraph import ResourceGraphClient

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

print("Clients initialized successfully")
