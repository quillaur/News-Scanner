import yaml
import sys
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import pandas as pd
from joblib import dump

params = yaml.safe_load(open("params.yaml"))["train"]

input = sys.argv[1]
output = sys.argv[2]

kernel = params["kernel"]
test_size = params["test_size"]

df = pd.read_csv(input)
y = df["target"]
X = df.drop(["target"], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

clf = SVC(kernel=kernel)

dump(clf, output) 