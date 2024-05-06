from dvclive import Live
import yaml
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from joblib import load

params = yaml.safe_load(open("params.yaml"))["evaluate"]

input = sys.argv[1]
model_path = sys.argv[2]

test_size = params["test_size"]

df = pd.read_csv(input)
y = df["target"]
X = df.drop(["target"], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

clf = load(model_path)

pred = clf.predict(X_test)
pred_proba = clf.predict_proba(X_test)

with Live("eval") as live:
    if not live.summary:
        live.summary = {"acc": {}, 
                        "recall": {},
                        "precision": {},
                        "f1": {}}
    live.summary["acc"]["test"] = accuracy_score(y_test, pred)
    live.summary["recall"]["test"] = recall_score(y_test, pred, average="weighted")
    live.summary["precision"]["test"] = precision_score(y_test, pred, average="weighted")
    live.summary["f1"]["test"] = f1_score(y_test, pred, average="weighted")

    live.log_sklearn_plot(
        "confusion_matrix",
        y_test.squeeze(),
        pred_proba.argmax(-1),
        name=f"cm/test",
    )