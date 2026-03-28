"""Employee attrition prediction project.

Expected dataset: HR-Employee.csv
Source referenced in the original notebook: IBM HR Analytics attrition dataset.

This script:
1. Loads the dataset
2. Cleans and encodes features
3. Splits the data into train and test sets
4. Trains Logistic Regression, Random Forest, and KNN models
5. Tunes Random Forest and KNN
6. Prints evaluation metrics
7. Saves confusion matrices and a model comparison chart
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42
TARGET = "Attrition"
DROP_COLUMNS = ["EmployeeNumber", "Over18", "StandardHours", "EmployeeCount"]


def load_data(csv_path: str | Path) -> pd.DataFrame:
    """Load the employee attrition dataset."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {csv_path}. Place HR-Employee.csv in the same folder as this script, "
            "or update the csv_path argument."
        )
    return pd.read_csv(csv_path)


def preprocess_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, list[str]]:
    """Clean and encode the dataset."""
    working_df = df.copy()

    missing = working_df.isnull().sum().sum()
    duplicates = working_df.duplicated().sum()
    print(f"Missing values in dataset: {missing}")
    print(f"Duplicate rows in dataset: {duplicates}")

    drop_cols = [col for col in DROP_COLUMNS if col in working_df.columns]
    if drop_cols:
        working_df = working_df.drop(columns=drop_cols)

    working_df[TARGET] = working_df[TARGET].map({"Yes": 1, "No": 0})

    categorical_cols = working_df.select_dtypes(include=["object"]).columns.tolist()
    print(f"Categorical columns encoded: {categorical_cols}")
    working_df = pd.get_dummies(working_df, drop_first=True)

    X = working_df.drop(columns=[TARGET])
    y = working_df[TARGET]
    return X, y, categorical_cols


def split_and_scale(X: pd.DataFrame, y: pd.Series):
    """Split data and scale features."""
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_raw)
    X_test = scaler.transform(X_test_raw)

    return X_train_raw, X_test_raw, X_train, X_test, y_train, y_test


def evaluate_model(model_name: str, y_true: pd.Series, y_pred, output_dir: Path) -> Dict[str, float]:
    """Print metrics and save confusion matrix."""
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print(f"\n{model_name}")
    print("-" * len(model_name))
    print(f"Accuracy: {acc:.4f}")
    print(f"F1 score: {f1:.4f}")
    print("Classification report:")
    print(classification_report(y_true, y_pred))

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Confusion Matrix - {model_name}")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    out_path = output_dir / f"{model_name.lower().replace(' ', '_')}_confusion_matrix.png"
    plt.savefig(out_path, dpi=200)
    plt.close()

    return {"accuracy": acc, "f1": f1}


def train_logistic_regression(X_train, y_train):
    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train, y_train):
    param_grid = {
        "n_estimators": [50, 100, 200],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5],
        "class_weight": [None, "balanced"],
    }
    grid = GridSearchCV(
        estimator=RandomForestClassifier(random_state=RANDOM_STATE),
        param_grid=param_grid,
        cv=5,
        scoring="f1",
        n_jobs=-1,
    )
    grid.fit(X_train, y_train)
    print("\nBest Random Forest parameters:", grid.best_params_)
    return grid.best_estimator_


def train_knn(X_train, y_train):
    k_range = range(1, 30, 2)
    cv_scores = []

    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, X_train, y_train, cv=5, scoring="f1")
        cv_scores.append(scores.mean())

    best_k = list(k_range)[cv_scores.index(max(cv_scores))]
    print(f"\nBest K for KNN: {best_k}")

    model = KNeighborsClassifier(n_neighbors=best_k)
    model.fit(X_train, y_train)
    return model, best_k


def save_model_comparison(results: Dict[str, Dict[str, float]], output_dir: Path) -> None:
    """Save a comparison chart for accuracy and F1 score."""
    model_names = list(results.keys())
    accuracies = [results[name]["accuracy"] for name in model_names]
    f1_scores = [results[name]["f1"] for name in model_names]

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.bar(model_names, accuracies)
    plt.title("Model Accuracy Comparison")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1)
    plt.xticks(rotation=15)

    plt.subplot(1, 2, 2)
    plt.bar(model_names, f1_scores)
    plt.title("Model F1 Score Comparison")
    plt.ylabel("F1 Score")
    plt.ylim(0, 1)
    plt.xticks(rotation=15)

    plt.tight_layout()
    plt.savefig(output_dir / "model_comparison.png", dpi=200)
    plt.close()


def main(csv_path: str | Path = "HR-Employee.csv") -> None:
    sns.set_theme(style="whitegrid")
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    df = load_data(csv_path)
    print(f"Dataset shape: {df.shape}")
    print("\nTarget distribution:")
    print(df[TARGET].value_counts())

    X, y, _ = preprocess_data(df)

    numeric_summary = pd.DataFrame(
        {
            "Mean": X.select_dtypes(include=["float64", "int64", "bool"]).mean(numeric_only=True),
            "Variance": X.select_dtypes(include=["float64", "int64", "bool"]).var(numeric_only=True),
            "Standard Deviation": X.select_dtypes(include=["float64", "int64", "bool"]).std(numeric_only=True),
        }
    )
    numeric_summary.to_csv(output_dir / "numeric_summary.csv")

    _, _, X_train, X_test, y_train, y_test = split_and_scale(X, y)

    results: Dict[str, Dict[str, float]] = {}

    logreg = train_logistic_regression(X_train, y_train)
    y_pred_logreg = logreg.predict(X_test)
    results["Logistic Regression"] = evaluate_model(
        "Logistic Regression", y_test, y_pred_logreg, output_dir
    )

    random_forest = train_random_forest(X_train, y_train)
    y_pred_rf = random_forest.predict(X_test)
    results["Random Forest"] = evaluate_model(
        "Random Forest", y_test, y_pred_rf, output_dir
    )

    knn, _ = train_knn(X_train, y_train)
    y_pred_knn = knn.predict(X_test)
    results["KNN"] = evaluate_model("KNN", y_test, y_pred_knn, output_dir)

    comparison_df = pd.DataFrame(results).T.reset_index().rename(columns={"index": "model"})
    comparison_df.to_csv(output_dir / "model_metrics.csv", index=False)
    save_model_comparison(results, output_dir)

    best_model = max(results.items(), key=lambda item: item[1]["f1"])
    print(
        f"\nRecommended model based on F1 score: {best_model[0]} "
        f"(F1 = {best_model[1]['f1']:.4f})"
    )


if __name__ == "__main__":
    main()
