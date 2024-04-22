import pandas as pd
import os
import sys
import yaml
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.svm import SVC
from dvclive import Live
from joblib import dump


in_path = sys.argv[1]
out_path = sys.argv[2]

params = yaml.safe_load(open("params.yaml"))["train"]
test_size = params["test_size"]
svc_kernel = params["svc_kernel"]

df = pd.read_csv(os.path.join(in_path, "preprocessed_ds.csv"))
X = df.drop("target", axis=1)
y = df["target"]

train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=test_size)

clf = SVC(kernel=svc_kernel)
clf.fit(train_x, train_y)

dump(clf, out_path)

pred = clf.predict(test_x)

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