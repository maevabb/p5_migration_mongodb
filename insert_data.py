import pandas as pd
import pymongo
from pymongo  import MongoClient, ASCENDING

#Connexion à MongoDB
client = MongoClient(host="localhost", port=27017) #connexion au serveur local
db = client["healthcare_db"] #Création de la bdd
collection = db["patients"] #Création de la collection

#Chargement du fichier CSV
df = pd.read_csv('healthcare_dataset.csv')

# Typage des données
df["Age"] = df["Age"].astype(int)  
df["Billing Amount"] = df["Billing Amount"].astype(float) 
df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
df["Discharge Date"] = pd.to_datetime(df["Discharge Date"]) 

#Conversion des données en dictionnaires
data = df.to_dict("records")

# Suppression des données existantes pour éviter les doublons
collection.delete_many({})

# Insertion des données dans MongoDB
collection.insert_many(data)

print("Données insérées avec succès dans MongoDB.")

# Création d'index
collection.create_index([("Name", ASCENDING)], unique=False)
collection.create_index([("Date of Admission", ASCENDING)], unique=False)

print("Données insérées avec succès dans MongoDB.")

# Conversion des documents MongoDB en DataFrame
cursor = collection.find({})
data = list(cursor)
df_export = pd.DataFrame(data)

# Sauvegarde en fichier CSV
df_export.to_csv('exported_healthcare_dataset.csv', index=False)

print("Données MongoDB exportées avec succès.")