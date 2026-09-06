from fastapi import FastAPI
import joblib
import pandas as pd
import logging
import json
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

logger = logging.getLogger("heart-disease-api")

app = FastAPI(
    title="Heart Disease Prediction API",
    description="API for predicting heart disease using a trained Logistic Regression model.",
    version="1.0.0"
)

model = joblib.load("heart_disease_model.pkl")

FEATURES = [
    "sno",
    "age",
    "gender",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal"
]


@app.get("/")
def root():
    return {
        "message": "Heart Disease Prediction API",
        "status": "healthy"
    }


@app.post("/predict")
def predict(features: dict):
    input_data = pd.DataFrame([features], columns=FEATURES)

    prediction = model.predict(input_data)[0]

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input_features": features,
        "prediction": prediction
    }

    logger.info(json.dumps(log_entry))

    return {
        "prediction": prediction
    }
