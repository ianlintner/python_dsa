# python-dsa - Azure AKS Deployment with OAuth2 Authentication

This directory contains Istio configuration to enable OAuth2 authentication for **python-dsa** on Azure AKS.

## Overview

- **Application**: python-dsa
- **Namespace**: default
- **Hostnames**: 
  - `dsa.cat-herding.net` (primary)
  - `dsa.hugecat.net` (legacy)
- **Port**: 80 (routes to container port 5000)
- **Gateway**: python-dsa-gateway

## What This Does

1. Routes requests from `dsa.cat-herding.net` and `dsa.hugecat.net` to your Flask application
2. Enforces authentication via oauth2-proxy using Istio ext_authz
3. Injects user identity headers into requests
4. Exempts health check endpoints (`/ping`) from authentication
5. Handles TLS termination with Let's Encrypt certificates

## Architecture

```
User Request → Istio Gateway (TLS termination)
            ↓
      VirtualService (routes to python-dsa.default.svc.cluster.local)
            ↓
      ext_authz check (oauth2-proxy provider)
            ↓
      [If authenticated] → python-dsa pod (Flask on port 5000)
      [If not] → 302 redirect to GitHub OAuth
```

## Deployment

```bash
# Apply the configuration from repository root
kubectl apply -k k8s/overlays/azure

# Verify resources
kubectl get virtualservice -n default python-dsa-virtualservice
kubectl get authorizationpolicy -n default python-dsa-require-auth
kubectl get authorizationpolicy -n default python-dsa-allow-healthcheck
kubectl get gateway -n default python-dsa-gateway
kubectl get certificate -n aks-istio-ingress
```

## Configuration Files

- `app.yaml` - Deployment, Service, and mTLS AuthorizationPolicy
- `authorization-policy-ext-authz.yaml` - OAuth2 authentication policies
- `virtualservice-default.yaml` - Traffic routing configuration
- `virtualservice-hugecat-redirect.yaml` - Apex domain redirect
- `gateway-default.yaml` - Istio Gateway (TLS + HTTP)
- `certificate-dsa-cat-herding.yaml` - TLS certificate for dsa.cat-herding.net
- `certificate-dsa-hugecat.yaml` - TLS certificate for dsa.hugecat.net
- `kustomization.yaml` - Kustomize resource aggregation

## Authentication Labels

Your application Deployment already has the required authentication label:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-dsa
  namespace: default
  labels:
    app: python-dsa
    auth.cat-herding.net/enabled: "true"  # ✓ Already configured
spec:
  selector:
    matchLabels:
      app: python-dsa
  template:
    metadata:
      labels:
        app: python-dsa
        auth.cat-herding.net/enabled: "true"  # ✓ Already configured
    spec:
      containers:
      - name: python-dsa
        image: gabby.azurecr.io/python-dsa:latest
        ports:
        - containerPort: 5000
```

## Access User Identity

Your Flask application receives these headers (already configured in `TRUSTED_PROXY_HEADERS`):

- `X-Auth-Request-User`: GitHub username
- `X-Auth-Request-Email`: User email address
- `X-Forwarded-User`: Alternative username header
- `X-Forwarded-Email`: Alternative email header
- `Authorization`: Bearer token (if configured)

### Example Usage in Flask

Your `flask_app/app.py` already has diagnostics logging enabled via `REQUEST_DIAGNOSTICS` env var:

```python
from flask import request

@app.route('/')
def index():
    email = request.headers.get('X-Auth-Request-Email')
    user = request.headers.get('X-Auth-Request-User')
    print(f"Authenticated user: {user} ({email})")
    return render_template('index.html', user=user, email=email)
```

Enable diagnostics in production:
```bash
kubectl set env deployment/python-dsa REQUEST_DIAGNOSTICS=true
```

## Testing

```bash
# Test unauthenticated access (should redirect to GitHub OAuth)
curl -I https://dsa.cat-herding.net/

# Expected: HTTP/1.1 302 Found
# Location: https://github.com/login/oauth/authorize?...

# Test with authenticated session cookie
curl -I -H "Cookie: _oauth2_proxy=YOUR_COOKIE_VALUE" https://dsa.cat-herding.net/

# Expected: HTTP/1.1 200 OK

# Test health endpoint (should bypass auth)
curl -I https://dsa.cat-herding.net/ping

# Expected: HTTP/1.1 200 OK
# {"status": "ok"}
```

## Troubleshooting

### Check VirtualService Routing
```bash
kubectl get virtualservice -n default python-dsa-virtualservice -o yaml
kubectl describe virtualservice -n default python-dsa-virtualservice
```

### Check Authorization Policies
```bash
kubectl get authorizationpolicy -n default | grep python-dsa
kubectl get authorizationpolicy -n default python-dsa-require-auth -o yaml
kubectl get authorizationpolicy -n default python-dsa-allow-healthcheck -o yaml
```

### View Application Logs
```bash
# Flask application logs
kubectl logs -n default -l app=python-dsa -f

# With diagnostics enabled
kubectl logs -n default -l app=python-dsa -f | grep -E '\[req\]|\[resp\]'
```

### View oauth2-proxy Logs (Cluster-Level)
```bash
# Find oauth2-proxy deployment
kubectl get deploy -A | grep oauth2-proxy

# View logs (adjust namespace as needed)
kubectl logs -n default -l app=oauth2-proxy -f
```

### Check Istio Gateway Configuration
```bash
kubectl get gateway -n default python-dsa-gateway -o yaml

# Check ingress gateway pods
kubectl get pods -n aks-istio-ingress -l istio=aks-istio-ingressgateway-external
kubectl logs -n aks-istio-ingress <ingress-pod-name> | grep ext_authz
```

### Check TLS Certificates
```bash
kubectl get certificate -n aks-istio-ingress
kubectl describe certificate -n aks-istio-ingress python-dsa-tls-cert
kubectl describe certificate -n aks-istio-ingress python-dsa-hugecat-tls-cert

# Check certificate secrets
kubectl get secret -n aks-istio-ingress python-dsa-tls-cert -o yaml
```

### Common Issues

**404 Not Found with `server: istio-envoy`**
- Problem: Host not matched by VirtualService or Gateway
- Check: `kubectl get virtualservice python-dsa-virtualservice -o jsonpath='{.spec.hosts}'`
- Should show: `["dsa.cat-herding.net","dsa.hugecat.net"]`

**Authentication Loop**
- Problem: oauth2-proxy redirect URL misconfigured or cookie domain mismatch
- Check cluster-level oauth2-proxy configuration
- Ensure `--redirect-url` includes your domain
- Ensure `--cookie-domain=.cat-herding.net`

**ext_authz Provider Not Found**
- Problem: Istio mesh config missing extensionProvider
- Check: `kubectl get configmap istio -n istio-system -o yaml | grep extensionProviders`
- Required: oauth2-proxy provider with envoyExtAuthzHttp configuration

**Health Check Fails**
- Problem: `/ping` endpoint requires auth
- Check: AuthorizationPolicy `python-dsa-allow-healthcheck` exists and is applied
- Verify: `kubectl get authorizationpolicy python-dsa-allow-healthcheck -o yaml`

### Test Without Auth (Debugging Only)

Temporarily disable authentication:
```bash
# Delete auth requirement policy (keeps health check exemption)
kubectl delete authorizationpolicy -n default python-dsa-require-auth

# Test direct access
curl -I https://dsa.cat-herding.net/

# Re-apply when done
kubectl apply -f k8s/overlays/azure/authorization-policy-ext-authz.yaml
```

## Disable Authentication Permanently

To remove authentication completely:

```bash
# Delete authorization policies
kubectl delete authorizationpolicy -n default python-dsa-require-auth
kubectl delete authorizationpolicy -n default python-dsa-allow-healthcheck

# Remove label from Deployment
kubectl label deployment -n default python-dsa auth.cat-herding.net/enabled-

# Or revert the entire overlay
# (Edit kustomization.yaml to remove authorization-policy-ext-authz.yaml)
kubectl apply -k k8s/overlays/azure
```

## Prerequisites (Cluster Administrator)

This configuration requires cluster-level Istio extensionProvider for oauth2-proxy:

```yaml
# In Istio ConfigMap (istio-system namespace)
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio
  namespace: istio-system
data:
  mesh: |
    extensionProviders:
    - name: oauth2-proxy
      envoyExtAuthzHttp:
        service: oauth2-proxy.default.svc.cluster.local
        port: 4180
        includeHeadersInCheck: ["authorization", "cookie"]
        headersToUpstreamOnAllow: 
          - "authorization"
          - "path"
          - "x-auth-request-user"
          - "x-auth-request-email"
          - "x-auth-request-preferred-username"
        headersToDownstreamOnDeny: 
          - "content-type"
          - "set-cookie"
        headersToDownstreamOnAllow:
          - "set-cookie"
```

Contact your cluster administrator if you see "no authorization policy provider found" errors.

## Additional Resources

- [Istio Authorization Policy](https://istio.io/latest/docs/reference/config/security/authorization-policy/)
- [Istio External Authorization](https://istio.io/latest/docs/tasks/security/authorization/authz-custom/)
- [OAuth2 Proxy Documentation](https://oauth2-proxy.github.io/oauth2-proxy/)
- [cert-manager Let's Encrypt](https://cert-manager.io/docs/configuration/acme/)

## Support

For issues with:
- **Application code**: Check `flask_app/app.py`
- **Routing/TLS**: Check VirtualService and Gateway configs
- **Authentication**: Check AuthorizationPolicy and cluster-level oauth2-proxy
- **Certificates**: Check cert-manager Certificate resources in aks-istio-ingress namespace
