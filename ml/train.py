import json
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

TRAINING_DATA_PATH = "ml/training_data.csv"
MODEL_OUTPUT_PATH = "ml/model.pkl"
FEATURE_ORDER_PATH = "ml/feature_order.json"

# Features with highest signal-to-noise for anomaly detection.
# Selected by comparing mean values between normal and anomalous samples.
# Using a focused subset avoids the "curse of dimensionality" that makes
# Isolation Forest ineffective with 99 mostly-similar features.
ML_FEATURES = [
    # Cold chain
    "hadColdChainBreak",
    "coldChainBreakCount",
    "totalBreakDurationMinutes",
    "coldChainBreaks_maxTemperatureReached",
    "coldChainBreaks_totalDurationMinutes",
    "tempIsWithinRange",
    # Microbiology (massive scale differences — strongest signal)
    "pathogensDetectedCount",
    "pathogensCfuPerGramMax",
    "pathogensLimitExceededCount",
    "microbiologicalCfuPerGramMax",
    "microbiologicalLimitExceededCount",
    # Chemical
    "chemicalMrlExceededCount",
    "substancesLimitExceededCount",
    "chemicalMeasuredValueMax",
    # Laboratory
    "legalLimitsExceeded",
    "overallVerdictFail",
    "exceedanceCount",
    "nutritionalDeviationPercent",
    "physicalOutOfSpecCount",
    # Allergens / visual
    "allergenLabelIncorrectCount",
    "moldDetected",
    "foreignBodyDetected",
    # Alerts / traceability
    "alertsTotalCount",
    "alertsSeverityMax",
    "alertsActiveCount",
    "traceabilityHasGaps",
    "traceabilityCompleteness",
    "unknownStations",
]


def train():
    df = pd.read_csv(TRAINING_DATA_PATH)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    df = df.fillna(0)

    # Train ONLY on normal/sparse-normal rows — exclude the synthetic anomalies.
    # Isolation Forest learns what "normal" looks like; anomalies in training
    # data corrupt that baseline and reduce detection accuracy.
    anomaly_mask = (
        (df["hadColdChainBreak"] > 0)
        | (df["pathogensDetectedCount"] > 0)
        | (df["chemicalMrlExceededCount"] > 0)
        | (df["legalLimitsExceeded"] > 0)
        | (df["alertsSeverityMax"] >= 3)
    )
    normal_df = df[~anomaly_mask]
    print(f"Training on {len(normal_df)} normal rows (excluded {anomaly_mask.sum()} anomalous)")

    # Use focused feature set instead of all 99 columns.
    X = normal_df[ML_FEATURES]

    with open(FEATURE_ORDER_PATH, "w") as f:
        json.dump(ML_FEATURES, f)
    print(f"Saved feature order ({len(ML_FEATURES)} features) -> {FEATURE_ORDER_PATH}")

    # contamination: expected fraction of outliers at inference time.
    # ~5% is a realistic false-positive budget for food safety checks.
    model = IsolationForest(n_estimators=200, contamination=0.05, random_state=42)
    model.fit(X)

    joblib.dump(model, MODEL_OUTPUT_PATH)
    print(f"Model trained and saved -> {MODEL_OUTPUT_PATH}")


if __name__ == "__main__":
    train()
