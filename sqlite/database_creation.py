import sqlite3
import os
from datetime import datetime

# Création de la base de données SQLite
db_filename = "sqlite/articles.db"

# Vérifier si la base de données existe déjà, si oui, la supprimer
if os.path.exists(db_filename):
    os.remove(db_filename)

# Se connecter à la base de données SQLite
conn = sqlite3.connect(db_filename)

cursor = conn.cursor()

# Créer une table pour stocker les auteurs
cursor.execute('''
    CREATE TABLE auteurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT
    )
''')

# Créer une table pour stocker les articles et les indicateurs
cursor.execute('''
    CREATE TABLE articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT,
        auteur_id INTEGER,
        date_publication DATE,
        nbr_mots INTEGER,
        FOREIGN KEY(auteur_id) REFERENCES auteurs(id)
    )
''')


for root, dirs, files in os.walk("articles"):
    for file in files:
        if file.startswith("post"):
            filename = os.path.join(root, file)
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().split("\n")
                title = content[0]
                auteur = content[1].split()
                auteur = auteur[1] + " " + auteur[2]
                date = content[2]
                # Conversion en objet datetime
                date_obj = datetime.strptime(date, "%B %d, %Y")
                # Conversion en format "YYYY-MM-DD"
                date_formatted = date_obj.strftime("%Y-%m-%d")

                nbr_mots = sum([len(e.split()) for e in content])

            print(title)
            print(auteur)
            print(date_formatted)
            print(nbr_mots)
            print("\n")

            cursor.execute('''
                INSERT INTO auteurs (nom)
                VALUES (:nom)
            ''', [auteur])


            # Exemple d'insertion d'un article avec des indicateurs
            article1 = {
                'titre': title,
                'auteur_id': cursor.lastrowid,
                'date_publication': date_formatted,
                'nbr_mots': nbr_mots
            }

            # Exécutez une requête d'insertion pour ajouter l'article à la base de données
            cursor.execute('''
                INSERT INTO articles (titre, auteur_id, date_publication, nbr_mots)
                VALUES (:titre, :auteur_id, :date_publication, :nbr_mots)
            ''', article1)

# Valider les modifications et fermer la connexion
conn.commit()
conn.close()

print("Base de données créée et articles insérés avec succès.")
