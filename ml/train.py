import json
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest

TRAINING_DATA_PATH = "ml/training_data.csv"
MODEL_OUTPUT_PATH = "ml/model.pkl"
FEATURE_ORDER_PATH = "ml/feature_order.json"


def train():
    df = pd.read_csv(TRAINING_DATA_PATH)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    df = df.fillna(0)

    feature_order = list(df.columns)
    with open(FEATURE_ORDER_PATH, "w") as f:
        json.dump(feature_order, f)
    print(f"Saved feature order ({len(feature_order)} features) -> {FEATURE_ORDER_PATH}")

    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(df)

    joblib.dump(model, MODEL_OUTPUT_PATH)
    print(f"Model trained and saved -> {MODEL_OUTPUT_PATH}")


if __name__ == "__main__":
    train()
