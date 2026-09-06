import pandas as pd
from scipy.stats import ks_2samp

TRAIN_FILE = "data/data.csv"
PRED_FILE = "data/prediction_data_100.csv"
OUTPUT_FILE = "data/drift_analysis.csv"

train_df = pd.read_csv(TRAIN_FILE)
pred_df = pd.read_csv(PRED_FILE)

# Use the same gender encoding as the model training pipeline
train_df["gender"] = pd.factorize(train_df["gender"])[0]

features = [
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

results = []

for feature in features:

    train_values = pd.to_numeric(
        train_df[feature],
        errors="coerce"
    ).dropna()

    prediction_values = pd.to_numeric(
        pred_df[feature],
        errors="coerce"
    ).dropna()

    statistic, p_value = ks_2samp(
        train_values,
        prediction_values
    )

    results.append({
        "feature": feature,
        "ks_statistic": round(statistic, 4),
        "p_value": round(p_value, 4),
        "drift_detected": p_value < 0.05
    })

drift_df = pd.DataFrame(results)

drift_df = drift_df.sort_values(
    "ks_statistic",
    ascending=False
)

drift_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("D7 — Input Drift Analysis")
print("=" * 70)
print(drift_df.to_string(index=False))

print("\nFeatures with detected drift (p < 0.05):")

drifted_features = drift_df.loc[
    drift_df["drift_detected"],
    "feature"
].tolist()

print(drifted_features)

print(
    "\nTotal features with detected drift:",
    len(drifted_features)
)

print("\nSaved to:", OUTPUT_FILE)
