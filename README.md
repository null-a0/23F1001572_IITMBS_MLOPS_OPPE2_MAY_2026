# OPPE-2 — Heart Disease Prediction

## Deliverable 1 — Private Git Repository

Private GitHub repository created with the required OPPE-2 naming convention.

## Deliverable 2 — Model Explainability

SHAP was used with the trained Logistic Regression model.

The least impactful features based on mean absolute SHAP value were:

- `exang`
- `thal`
- `fbs`
- `gender`

## Deliverable 3 — Fairness Testing

Fairlearn was used with `age` as the sensitive attribute.

Fairness disparities:

- Selection rate difference: 0.0
- True positive rate difference: 0.0
- False positive rate difference: 0.1

## Deliverable 4 — Dockerized API Deployment on GKE

The trained heart disease model was exposed through a FastAPI REST API and containerized using Docker.

The Docker image was pushed to Google Artifact Registry and deployed to Google Kubernetes Engine (GKE).

Kubernetes resources:

- Deployment: `heart-disease-api`
- Service: `heart-disease-api-service`
- Service type: `LoadBalancer`
- HPA minimum pods: 1
- HPA maximum pods: 3
- CPU target: 70%

GitHub Actions provides CI/CD for the application. On every push to `main`, the workflow:

1. Builds the Docker image.
2. Pushes the image to Artifact Registry.
3. Authenticates with GKE.
4. Deploys the application to GKE.
5. Applies the Kubernetes Service and HPA.
6. Verifies the deployment.

The GKE API health endpoint and prediction endpoint were successfully tested.
