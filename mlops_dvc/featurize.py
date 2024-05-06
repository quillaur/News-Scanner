import yaml
import sys
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA


params = yaml.safe_load(open("params.yaml"))["featurize"]
max_samples = params["max_samples"]
min_df = params["min_df"]
pca_ratio = params["pca_ratio"]

df = pd.read_csv(os.path.join("dataset", "train.csv"))
df = df.sample(max_samples, random_state=0).reset_index(drop=True)

vectorizer = TfidfVectorizer(stop_words="english", min_df=0.01)
X = vectorizer.fit_transform(df["Title"])

res = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

pca = PCA(n_components=pca_ratio)
pca.fit(res)
X = pca.fit_transform(res)
df1 = pd.DataFrame(X, columns=range(pca.n_components_))
df1["target"] = df["Class Index"]
df1.to_csv(os.path.join("dataset", "preprocessed_ds.csv"), index=False)