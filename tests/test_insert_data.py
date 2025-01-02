import pytest
import pandas as pd
import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Fixture pour la connexion MongoDB
@pytest.fixture
def mongo_client():
    """Fixture pour la connexion à MongoDB"""
    client = MongoClient(host="localhost", port=27017)
    yield client
    client.close()

# Fixture pour charger les données du CSV
@pytest.fixture
def healthcare_data():
    """Charge les données du fichier CSV"""
    df = pd.read_csv('healthcare_dataset.csv')

    # Typage des données
    df["Age"] = df["Age"].astype(int)
    df["Billing Amount"] = df["Billing Amount"].astype(float)
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
    df["Discharge Date"] = pd.to_datetime(df["Discharge Date"])

    return df

# Fixture pour exporter les données depuis MongoDB
@pytest.fixture
def export_healthcare_data(mongo_client):
    """Export des données de MongoDB vers un fichier CSV"""
    db = mongo_client["test_healthcare_db"]
    collection = db["test_patients"]

    # Export des données de MongoDB vers un fichier CSV
    cursor = collection.find({}, {"_id": 0})
    data_from_mongo = list(cursor)
    df_exported = pd.DataFrame(data_from_mongo)
    df_exported.to_csv('exported_healthcare_dataset.csv', index=False)

    return df_exported


def test_data_insertion(mongo_client, healthcare_data):
    """Test pour vérifier que les données sont insérées dans MongoDB"""

    db = mongo_client["test_healthcare_db"]
    collection = db["test_patients"]

    # Suppression des anciennes données
    collection.delete_many({})

    # Conversion des données en dictionnaires et insertion
    data = healthcare_data.to_dict("records")
    collection.insert_many(data)

    # Vérification du nombre de documents
    assert collection.count_documents({}) == len(healthcare_data), "Le nombre de documents insérés ne correspond pas."

def test_data_integrity(mongo_client, healthcare_data):
    """Test d'intégrité des données pour vérifier doublons et types"""

    db = mongo_client["test_healthcare_db"]
    collection = db["test_patients"]

    # Conversion des données en dictionnaires et insertion
    data = healthcare_data.to_dict("records")
    collection.delete_many({})  # Supprime les anciennes données
    collection.insert_many(data)

    # Vérification des colonnes
    expected_columns = [
        "Name", "Age", "Gender", "Blood Type", "Medical Condition", 
        "Date of Admission", "Doctor", "Hospital", "Insurance Provider", 
        "Billing Amount", "Room Number", "Admission Type", "Discharge Date", 
        "Medication", "Test Results"
    ]

    # Récupération des colonnes des documents et vérification de leur présence et de leurs valeurs
    for record in collection.find():

        for column in expected_columns:
            assert column in record, f"Colonne manquante dans un document : {column}"
            assert record[column] not in [None, ""], f"Valeur manquante ou vide pour la colonne {column} dans {record['Name']}"


      # Vérification des types de données
    for record in collection.find():
        assert isinstance(record["Age"], int), f"Age invalide pour {record['Name']}"
        assert isinstance(record["Billing Amount"], float), f"Billing Amount invalide pour {record['Name']}"
        assert isinstance(record["Date of Admission"], datetime.datetime), f"Date of Admission invalide pour {record['Name']}"
        assert isinstance(record["Discharge Date"], datetime.datetime), f"Discharge Date invalide pour {record['Name']}"

    # Test des doublons (basé sur Name, Date of Admission, Discharge Date)
    duplicates = collection.aggregate([
        {
            "$group": {
                "_id": {"name": "$Name", "admission": "$Date of Admission", "discharge": "$Discharge Date"},
                "count": {"$sum": 1}
            }
        },
        {"$match": {"count": {"$gt": 1}}}
    ])

    assert list(duplicates) == [], "Des doublons ont été trouvés dans la base de données."

    print("Test d'intégrité des données réussi.")


def test_export_integrity(mongo_client, healthcare_data, export_healthcare_data):
    """Test pour vérifier l'intégrité des données après exportation depuis MongoDB"""
    
    # Test 1: Vérification du nombre de lignes
    assert len(healthcare_data) == len(export_healthcare_data), "Le nombre de lignes ne correspond pas entre le fichier d'origine et le fichier exporté."

    # Test 2: Vérification des colonnes
    assert list(healthcare_data.columns) == list(export_healthcare_data.columns), "Les colonnes ne correspondent pas entre le fichier d'origine et le fichier exporté."

    # Test 3: Comparaison des valeurs pour les premières lignes
    for col in healthcare_data.columns:
        for i in range(min(5, len(healthcare_data))):  # Vérification des 5 premières lignes
            assert healthcare_data.iloc[i][col] == export_healthcare_data.iloc[i][col], f"Valeur différente pour {col} à la ligne {i+1}"

    print("Test d'intégrité de l'export réussi.")