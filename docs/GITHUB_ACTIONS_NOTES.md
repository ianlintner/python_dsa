# GitHub Actions Workflow Notes

## CI Workflow Overview

The repository uses a GitHub Actions workflow defined in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).

### Triggers

- `push` on the **`main` branch** and version tags (`v*`).
- `pull_request` targeting **`main`**.
- Manual runs via **workflow_dispatch** when needed.

> The workflow also uses `concurrency` to ensure only the latest run per ref/PR stays active, which keeps pending check counts low.

### Jobs

1. **Tests**
   - Runs on Python 3.10, 3.11, and 3.12.
   - Installs dependencies with pip.
   - Runs `pre-commit` checks (lint, format, misc).
   - Executes the test suite with `pytest`.
   - Uploads `coverage.xml` as an artifact.

2. **Docker Build & Push**

- Runs only for `push` events on `main` (or tagged releases) after tests succeed.
- Authenticates to Azure using [`azure/login`](https://github.com/Azure/login) with the `AZURE_CREDENTIALS` secret (JSON output from `az ad sp create-for-rbac --sdk-auth`).
- Logs in to Azure Container Registry (ACR) `gabby`.
- Uses `docker/setup-buildx-action` + `docker/metadata-action` for reproducible builds with cache reuse.
- Builds and pushes the Docker image to `gabby.azurecr.io/python-dsa` with tags: `latest` (default branch), branch/tag refs, and the commit SHA.

### Azure Service Principal Setup

- **Recommended**: configure GitHub OIDC federation with Azure AD so the workflow can exchange short-lived tokens without storing long-lived client secrets. This avoids the deprecated `--sdk-auth` flow and removes the need for the `AZURE_CREDENTIALS` secret. Follow the [federated credential guide](https://learn.microsoft.com/azure/active-directory/develop/workload-identity-federation-create-trust-github) to create an app registration, add a federated credential for your repo, and assign the `AcrPush` role to the app.

- **Legacy fallback**: if you must keep using a client secret, create (or reuse) a service principal with `AcrPush` permissions on the `gabby` registry and store the JSON output as the `AZURE_CREDENTIALS` secret. Note that `--sdk-auth` is deprecated and may be removed in future CLI versions, so migrate when possible.

  ```bash
  az ad sp create-for-rbac \
    --name python-dsa-github-ci \
    --role AcrPush \
    --scopes /subscriptions/79307c77-54c3-4738-be2a-dc96da7464d9/resourceGroups/nekoc/providers/Microsoft.ContainerRegistry/registries/gabby \
    --sdk-auth
  ```

### Notes

- If you encounter `AADSTS700016`/`invalid_client` errors, confirm the JSON in `AZURE_CREDENTIALS` matches the service principal used for `azure/login`.
- The service principal must have at least `AcrPush` on the target registry.
- Use `workflow_dispatch` for manual runs:

  ```bash
  gh workflow run CI --ref main
