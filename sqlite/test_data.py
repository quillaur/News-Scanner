import sqlite3

# Se connecter à la base de données SQLite
conn = sqlite3.connect("sqlite/articles.db")

# Créer un curseur pour exécuter des requêtes SQL
cursor = conn.cursor()

# Exemple de requête : Sélectionnez tous les articles
cursor.execute("SELECT * FROM articles INNER JOIN auteurs ON articles.auteur_id = auteurs.id")

# Récupérez tous les résultats de la requête
articles = cursor.fetchall()

# Afficher les articles
for article in articles:
    print(article)
    print("ID:", article[0])
    print("Titre:", article[1])
    print("Auteur ID:", article[2])
    print("Auteur:", article[6])
    print("Date de publication:", article[3])
    print("Nombre de mots", article[4])
    print("\n")

# Fermer la connexion à la base de données
conn.close()
