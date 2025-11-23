# GitHub Actions Workflow Notes

## CI Workflow Overview

The repository uses a GitHub Actions workflow defined in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).

### Triggers

- Runs on **all branches** (`push`).
- Runs on **pull requests**.
- Can be triggered manually via **workflow_dispatch**.

### Jobs

1. **Tests**
   - Runs on Python 3.10, 3.11, and 3.12.
   - Installs dependencies with pip.
   - Runs `pre-commit` checks (lint, format, misc).
   - Executes the test suite with `pytest`.
   - Uploads `coverage.xml` as an artifact.

2. **Docker Build & Push**
   - Runs after tests succeed.
   - Authenticates to Azure using [`azure/login`](https://github.com/Azure/login) with the `AZURE_CREDENTIALS` secret (JSON output from `az ad sp create-for-rbac --sdk-auth`).
   - Logs in to Azure Container Registry (ACR) `gabby`.
   - Builds and pushes the Docker image to `gabby.azurecr.io/python-dsa:latest`.

### Azure Service Principal Setup

- Create (or reuse) a service principal with AcrPush permissions on the `gabby` registry and store the JSON output as the `AZURE_CREDENTIALS` secret:

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
