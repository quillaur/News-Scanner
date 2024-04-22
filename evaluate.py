import pandas as pd
import os
from dvclive import Live
from joblib import load
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.model_selection import train_test_split
import sys
import yaml

params = yaml.safe_load(open("params.yaml"))["evaluate"]
test_size = params["test_size"]

ds_path = sys.argv[1]
model_path = sys.argv[2]

clf = load(model_path)

df = pd.read_csv(ds_path)
X = df.drop("target", axis=1)
y = df["target"]
train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=test_size)

pred = clf.predict(test_x)
pred_proba = clf.predict_proba(test_x)

EVAL_PATH = "eval"
with Live(EVAL_PATH) as live:
    if not live.summary:
        live.summary = {"acc": {}, 
                        "recall": {},
                        "precision": {},
                        "f1": {}}
    live.summary["acc"]["test"] = accuracy_score(test_y, pred)
    live.summary["recall"]["test"] = recall_score(test_y, pred, average="weighted")
    live.summary["precision"]["test"] = precision_score(test_y, pred, average="weighted")
    live.summary["f1"]["test"] = f1_score(test_y, pred, average="weighted")

    live.log_sklearn_plot(
        "confusion_matrix",
        test_y.squeeze(),
        pred_proba.argmax(-1),
        name=f"cm/test",
    )