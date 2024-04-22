import pandas as pd
import os
import sys
import yaml
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
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

clf = SVC(kernel=svc_kernel, probability=True)
clf.fit(train_x, train_y)

dump(clf, out_path)