import streamlit as st
import sqlite3
from collections import defaultdict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def get_data():
    # Se connecter à la base de données SQLite
    conn = sqlite3.connect("sqlite/articles.db")

    # Créer un curseur pour exécuter des requêtes SQL
    cursor = conn.cursor()

    # Exemple de requête : Sélectionnez tous les articles
    cursor.execute("SELECT * FROM articles INNER JOIN auteurs ON articles.auteur_id = auteurs.id")

    # Récupérez tous les résultats de la requête
    articles = cursor.fetchall()

    conn.close()

    articles_data = defaultdict(list)
    # Afficher les articles
    for article in articles:
        articles_data["ID"].append(article[0])
        articles_data["Titre"].append(article[1])
        articles_data["Auteur"].append(article[6])
        articles_data["Date"].append(article[3])
        articles_data["NB mots"].append(article[4])

    df = pd.DataFrame(articles_data)
    df.set_index("ID", inplace=True)
    return df


if __name__ == "__main__":
    st.title("News Scanner KPI")
    st.subheader("Data training")

    name = st.sidebar.text_input("Nom d'auteur:")

    df = get_data()

    if name:
        mask = (df["Auteur"] == name)
        df = df[mask]

    date = df["Date"].unique()
    nb_articles = df["Date"].value_counts().to_numpy()
    y_pos = list(range(len(date)))

    fig, ax = plt.subplots()
    ax.plot(date, nb_articles)
    ax.set_xticks(y_pos, date, rotation=20)

    col1, col2 = st.columns([2,1])

    with col1:
        st.pyplot(fig)
    
    with col2:
        st.dataframe(df["Auteur"].value_counts())
    
    


