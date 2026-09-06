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

## Deliverable 5 — Prediction Logging and Observability

A random dataset containing 100 input samples was generated and each sample was sent individually to the deployed prediction API.

The API logs each prediction request with:
- Timestamp
- Input features
- Predicted output

All 100 API requests were successful.

Prediction results:
- `no`: 59
- `yes`: 41

The container logs were verified using Kubernetes logs, showing the timestamp, input features, and prediction for individual requests. GCP Cloud Logging was also queried and returned 100 recent container log entries.

The prediction dataset and resulting predictions are stored in:
- `data/prediction_data_100.csv`
- `data/predictions_100.csv`

## Deliverable 6 — Stress Testing

The deployed prediction API was stress tested using `wrk` with more than 2,000 concurrent connections.

Test configuration:
- Threads: 4
- Concurrent connections: 2,001
- Duration: 30 seconds
- Request timeout: 10 seconds

Results:
- Total requests: 3,432
- Throughput: 114.32 requests/sec
- Average latency: 6.37 seconds
- Median latency: 6.38 seconds
- 75th percentile latency: 8.28 seconds
- 90th percentile latency: 9.29 seconds
- 99th percentile latency: 9.90 seconds
- Connect errors: 0
- Read errors: 0
- Write errors: 0
- Timeouts: 2,477

During the stress test, the HPA reached 200% CPU utilization against the 70% target and scaled the deployment to 3 replicas, which is the configured maximum.

The API remained reachable with no connection, read, or write errors, but significant latency and timeout pressure was observed under 2,001 concurrent connections.

## Deliverable 7 — Input Drift Analysis

Input drift was analyzed by comparing the original training dataset with the 100-row generated prediction dataset.

The Kolmogorov-Smirnov (KS) two-sample test was used for the 14 input features. A feature was considered to have statistically significant drift when the p-value was less than 0.05.

Results:
- Features with detected drift: 11 out of 14
- Features without detected drift: 3 out of 14

Features with detected drift:
- `thal` — KS statistic: 0.5340, p-value: 0.0000
- `oldpeak` — KS statistic: 0.5150, p-value: 0.0000
- `chol` — KS statistic: 0.5002, p-value: 0.0000
- `ca` — KS statistic: 0.4476, p-value: 0.0000
- `fbs` — KS statistic: 0.4215, p-value: 0.0000
- `trestbps` — KS statistic: 0.3630, p-value: 0.0000
- `restecg` — KS statistic: 0.3468, p-value: 0.0000
- `thalach` — KS statistic: 0.3463, p-value: 0.0000
- `slope` — KS statistic: 0.2207, p-value: 0.0011
- `cp` — KS statistic: 0.1841, p-value: 0.0103
- `age` — KS statistic: 0.1673, p-value: 0.0256

Features without statistically significant drift:
- `exang` — p-value: 0.0513
- `gender` — p-value: 0.1847
- `sno` — p-value: 0.6388

The analysis indicates that the generated prediction data has substantial distribution differences from the training data for 11 of the 14 input features. This does not by itself indicate incorrect predictions; it indicates that the input distribution has changed and should be monitored in a production environment.

The drift analysis implementation and results are stored in:
- `drift_analysis.py`
- `data/drift_analysis.csv`
