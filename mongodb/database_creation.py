import pymongo
from datetime import datetime
import os

# Connexion à la base de données MongoDB (assurez-vous que MongoDB est en cours d'exécution)
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Créez une nouvelle base de données ou utilisez une existante
db = client["news"]

# Créez une collection pour stocker les articles
collection = db["articles"]


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

                contenu = "\n".join(content[3:])

            print(title)
            print(auteur)
            print(date_formatted)
            print("\n")

            article = {
                "titre": title,
                "contenu": contenu,
                "auteur": auteur,
                "date": date_formatted
            }
            collection.insert_one(article)

# Fermez la connexion MongoDB
client.close()
