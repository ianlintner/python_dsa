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
   - Authenticates to Google Cloud using **Workload Identity Federation (WIF)**:
     - Workload Identity Provider:
       `projects/316518955652/locations/global/workloadIdentityPools/github-pool/providers/github-oidc`
     - Service Account:
       `kame-house-oidc@kame-457417.iam.gserviceaccount.com`
   - Configures Docker for Artifact Registry.
   - Builds and pushes the Docker image to:
     `us-central1-docker.pkg.dev/kame-457417/python-dsa/python-dsa:latest`

### Workload Identity Federation (WIF) Setup
- The service account is bound with:
  ```bash
  gcloud iam service-accounts add-iam-policy-binding \
    ${{ GCP_SERVICE_ACCOUNT }} \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/projects/${{ GCP_PROJECT_NUMBER }}/locations/global/workloadIdentityPools/${{ GCP_WIF_POOL }}/attribute.repository/ianlintner/python_dsa"
  ```

### Notes
- If you encounter `unauthorized_client` errors, check the **attribute condition** on the WIF provider in GCP.
- Ensure the service account has the correct roles (e.g., `roles/artifactregistry.writer`).
- Use `workflow_dispatch` for manual runs:
  ```bash
  gh workflow run CI --ref main
