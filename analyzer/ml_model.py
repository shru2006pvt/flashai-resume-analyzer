import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

LABEL_TO_TEXT = {
    0: "Low Match",
    1: "Moderate Match",
    2: "Good Match",
    3: "Excellent Match",
}


def load_training_data(data_path):
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        return df

    rows = [
        {"semantic_similarity": 0.88, "skill_match": 0.9, "experience": 0.9, "education": 0.9, "project": 0.8, "ats": 0.9, "label": 3},
        {"semantic_similarity": 0.75, "skill_match": 0.72, "experience": 0.7, "education": 0.7, "project": 0.6, "ats": 0.8, "label": 2},
        {"semantic_similarity": 0.5, "skill_match": 0.45, "experience": 0.5, "education": 0.4, "project": 0.45, "ats": 0.6, "label": 1},
        {"semantic_similarity": 0.2, "skill_match": 0.2, "experience": 0.2, "education": 0.2, "project": 0.15, "ats": 0.35, "label": 0},
        {"semantic_similarity": 0.68, "skill_match": 0.65, "experience": 0.8, "education": 0.7, "project": 0.5, "ats": 0.75, "label": 2},
        {"semantic_similarity": 0.92, "skill_match": 0.95, "experience": 0.95, "education": 0.95, "project": 0.9, "ats": 0.95, "label": 3},
    ]
    return pd.DataFrame(rows)


def build_model():
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    solver="lbfgs",
                    max_iter=400,
                    random_state=42,
                ),
            ),
        ]
    )


MODEL = None


def load_or_train_model(data_path):
    global MODEL
    df = load_training_data(data_path)
    features = ["semantic_similarity", "skill_match", "experience", "education", "project", "ats"]
    X = df[features]
    y = df["label"]
    model = build_model()
    model.fit(X, y)
    MODEL = model
    return MODEL


def predict_fit_level(feature_dict):
    global MODEL
    if MODEL is None:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_training.csv")
        load_or_train_model(data_path)

    features = [
        feature_dict.get("semantic_similarity", 0.0),
        feature_dict.get("skill_match", 0.0),
        feature_dict.get("experience", 0.0),
        feature_dict.get("education", 0.0),
        feature_dict.get("project", 0.0),
        feature_dict.get("ats", 0.0),
    ]
    prediction = MODEL.predict([features])[0]
    return LABEL_TO_TEXT.get(int(prediction), "Moderate Match")
