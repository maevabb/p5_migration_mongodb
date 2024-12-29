import pandas as pd
import pymongo
from pymongo  import MongoClient

#Connexion à MongoDB
client = MongoClient(host="localhost", port=27017) #connexion au serveur local
db = client["healthcare_db"] #Création de la bdd
collection = db["patients"] #Création de la collection

#Chargement du fichier CSV
df = pd.read_csv('healthcare_dataset.csv')

#Conversion des données en dictionnaires
data = df.to_dict("records")

# Insertion des données dans MongoDB
collection.insert_many(data)

print("Données insérées avec succès dans MongoDB")