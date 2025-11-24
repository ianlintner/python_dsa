#!/bin/bash
# Script to create DNS A record for dsa.hugecat.net in Azure DNS

set -e

echo "=== Creating DNS A record for dsa.hugecat.net ==="

# Configuration
DNS_ZONE="hugecat.net"
RECORD_NAME="dsa"
RESOURCE_GROUP="${RESOURCE_GROUP:-}"

# Get the external IP of the Istio ingress gateway
echo "Getting Istio ingress gateway external IP..."
GATEWAY_IP=$(kubectl get svc -n aks-istio-ingress aks-istio-ingressgateway-external -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

if [ -z "$GATEWAY_IP" ]; then
    echo "ERROR: Could not get gateway IP. Please check your Kubernetes cluster connection."
    exit 1
fi

echo "Gateway IP: $GATEWAY_IP"

# Find the resource group for the DNS zone if not specified
if [ -z "$RESOURCE_GROUP" ]; then
    echo "Finding resource group for DNS zone $DNS_ZONE..."
    RESOURCE_GROUP=$(az network dns zone list --query "[?name=='$DNS_ZONE'].resourceGroup | [0]" -o tsv)
    
    if [ -z "$RESOURCE_GROUP" ]; then
        echo "ERROR: Could not find resource group for DNS zone $DNS_ZONE"
        echo "Please set RESOURCE_GROUP environment variable or create the DNS zone first."
        exit 1
    fi
    
    echo "Found resource group: $RESOURCE_GROUP"
fi

# Create or update the A record
echo "Creating/updating A record..."
az network dns record-set a add-record \
    --resource-group "$RESOURCE_GROUP" \
    --zone-name "$DNS_ZONE" \
    --record-set-name "$RECORD_NAME" \
    --ipv4-address "$GATEWAY_IP"

echo ""
echo "✅ DNS A record created successfully!"
echo "   Domain: $RECORD_NAME.$DNS_ZONE"
echo "   Points to: $GATEWAY_IP"
echo ""
echo "Note: DNS propagation may take a few minutes."
echo "You can check the record with:"
echo "  dig $RECORD_NAME.$DNS_ZONE"
echo "  nslookup $RECORD_NAME.$DNS_ZONE"
