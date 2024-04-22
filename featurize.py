import yaml
from sklearn.decomposition import PCA
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import sys

params = yaml.safe_load(open("params.yaml"))["featurize"]
max_sample = params["max_sample"]
min_df = params["min_df"]
pca_ratio = params["pca_ratio"]

in_path = sys.argv[1]
out_path = sys.argv[2]

df = pd.read_csv(os.path.join(in_path, "train.csv"))
df = df.sample(max_sample, random_state=0).reset_index(drop=True)

vectorizer = TfidfVectorizer(stop_words="english", min_df=min_df)
X = vectorizer.fit_transform(df["Title"])
target = df["Class Index"]
res = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

pca = PCA(n_components=pca_ratio)
pca.fit(res)
X = pca.fit_transform(res)

df = pd.DataFrame(X, columns=range(pca.n_components_))
df["target"] = target
df.to_csv(out_path)