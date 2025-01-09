# Projet de Migration vers MongoDB avec Docker

**Dernière mise à jour : 9 janvier 2025**

Ce projet consiste à migrer des données médicales à partir d'un fichier CSV vers une base de données MongoDB, tout en utilisant Docker pour une gestion efficace de l'environnement.

## Prérequis

Avant de commencer, assurez-vous que vous avez les outils suivants installés sur votre machine :

- [Docker](https://www.docker.com/get-started) : pour exécuter les conteneurs.
- [Git](https://git-scm.com/) : pour cloner le dépôt.

> **Note :** Poetry est déjà installé et utilisé dans le conteneur Docker. Vous n'avez pas besoin de l'installer localement.

## Schéma de la Base de Données

### Structure de la collection

La base de données contient une seule collection : `patients`. Voici la structure de la collection :

| Champ                | Type     | Description                                                        |
|----------------------|----------|--------------------------------------------------------------------|
| `Name`               | string   | Nom du patient                                                     |
| `Age`                | int      | Âge du patient                                                     |
| `Gender`             | string   | Genre du patient                                                   |
| `Blood_Type`         | string   | Groupe sanguin du patient                                          |
| `Medical_Condition`  | string   | Pathologie principale du patient                                   |
| `Date_of_Admission`  | date     | Date d'admission à l'hôpital                                       |
| `Doctor`             | string   | Médecin en charge du patient                                       |
| `Hospital`           | string   | Nom de l'hôpital où le patient a été admis                         |
| `Insurance_Provider` | string   | Assureur du patient                                                |
| `Billing_Amount`     | float    | Montant de la facture associée au patient                          |
| `Room_Number`        | int      | Numéro de la chambre assignée au patient                           |
| `Admission_Type`     | string   | Type d'admission (Urgent, Emergency, etc.)                         |
| `Discharge_Date`     | date     | Date de sortie de l'hôpital                                        |
| `Medication`         | string   | Médication prescrite au patient                                    |
| `Test_Results`       | string   | Résultats des tests médicaux (Normal, Inconclusive, etc.)          |

Cette structure permet de capturer toutes les informations nécessaires pour analyser les données médicales des patients et effectuer des requêtes pertinentes sur la base de données.

### Exemple de document JSON

Voici un exemple de document issu de la collection `patients`, basé sur le dataset utilisé dans ce projet :

```json
{
  "Name": "Bob** Jac****",
  "Age": 30,
  "Gender": "Male",
  "Blood_Type": "B-",
  "Medical_Condition": "Cancer",
  "Date_of_Admission": "2024-01-31",
  "Doctor": "Matthew Smith",
  "Hospital": "Sons and Miller",
  "Insurance_Provider": "Blue Cross",
  "Billing_Amount": 18856.28,
  "Room_Number": 328,
  "Admission_Type": "Urgent",
  "Discharge_Date": "2024-02-02",
  "Medication": "Paracetamol",
  "Test_Results": "Normal"
}
```

## Installation

1. Clonez ce dépôt :

   ```bash
   git clone https://github.com/maevabb/p5_migration_mongodb
   cd p5_migration_mongodb
   ```

2. Copier le fichier csv healthcare_dataset.csv dans le dossier du projet

3. Démarrez les conteneurs Docker :

   ```bash
   docker-compose up --build
   ```

## Fonctionnement

Le projet est composé de deux services principaux :

1. **MongoDB** :
   - Utilise l'image `mongo:8.0.4`.
   - Les données sont persistées dans un volume Docker `mongo_data`.

2. **Application Python** :
   - Effectue les tests unitaires avec `pytest`.
   - Insère les données à partir d'un fichier CSV dans la base MongoDB si tous les tests réussissent.

   Les commandes suivantes sont exécutées dans le conteneur :

   ```bash
   poetry run pytest && poetry run python insert_data.py
   ```

Si les tests échouent, l'insertion des données n'aura pas lieu.

## Volumes Utilisés

- **mongo_data** : Stocke les données de MongoDB.
- **csv_data** (optionnel) : Peut être utilisé pour partager des fichiers CSV entre l'hôte et le conteneur.

## Développement et Tests

### Détail des Tests

Les tests unitaires sont une étape clé de ce projet. Ils garantissent que le script `insert_data.py` fonctionne correctement avant d'insérer les données dans MongoDB.

#### Objectifs des tests

Les tests unitaires (fichier `test_insert_data.py`) vérifient :

1. **Structure des données** :
   - Le fichier CSV est bien lu et contient toutes les colonnes nécessaires.
   - Les données sont correctement typées (ex. : dates, nombres, textes).
2. **Connexion à MongoDB** :
   - La connexion avec la base MongoDB est établie sans erreur.
   - La base de données et la collection sont bien créées.
3. **Insertion des données** :
   - Les doublons sont détectés et évités.
   - Les données insérées dans MongoDB correspondent aux données du fichier CSV.
4. **Indexation** :
   - Les index sur les champs critiques (comme `Name` et `Date of Admission`) sont correctement créés.

#### Exécution des tests

1. Les tests sont automatiquement exécutés lors du démarrage du conteneur `python-app`. Si les tests échouent, l'insertion des données ne sera pas effectuée.

2. Pour exécuter les tests manuellement dans le conteneur Python :
   ```bash
   docker exec -it python-app poetry run pytest
   ```

3. Exemple de sortie lors d'un test échoué :
   ```
   AssertionError: Les données du fichier CSV ne correspondent pas au format attendu.
   ```
   > Ce type de message permet d'identifier rapidement l'origine du problème.

#### Ajout de nouveaux tests

Pour ajouter des tests supplémentaires, créez un fichier dans le répertoire `tests` ou modifiez `test_insert_data.py`. Assurez-vous de suivre la convention d’écriture des tests avec Pytest.

## Structure du Projet

```
.
├── Dockerfile                # Définit l'image pour l'application Python
├── docker-compose.yml        # Gère les services Docker
├── insert_data.py            # Script d'insertion des données
├── tests                     # Répertoire contenant les test
│   └── test_insert_data.py
├── pyproject.toml            # Fichier de configuration Poetry
├── poetry.lock               # Fichier de verrouillage des dépendances
├── README.md                 # Documentation du projet
```

## Système d’authentification et rôles utilisateurs

### Authentification MongoDB

L'accès à la base de données MongoDB est sécurisé par plusieurs rôles d'utilisateurs. Voici la liste des rôles et des utilisateurs associés :

1. **Admin** :  
   - **Nom d’utilisateur** : `adminUser`  
   - **Mot de passe** : `adminpassword`  
   - **Rôles** : `readWrite`, `dbAdmin`, `clusterAdmin`  
   - **Accès** : Accès complet à MongoDB (gestion de la base de données et des utilisateurs).

2. **Utilisateur de lecture** :  
   - **Nom d’utilisateur** : `readOnlyUser`  
   - **Mot de passe** : `readonlypassword`  
   - **Rôles** : `read`  
   - **Accès** : Lecture seule dans la base de données.

3. **Utilisateur d'écriture** :  
   - **Nom d’utilisateur** : `writeUser`  
   - **Mot de passe** : `writepassword`  
   - **Rôles** : `readWrite`  
   - **Accès** : Lecture et écriture dans la base de données.

4. **Support** :  
   - **Nom d’utilisateur** : `supportUser`  
   - **Mot de passe** : `supportpassword`  
   - **Rôles** : `read`, `readWrite`, `dbAdmin`  
   - **Accès** : Accès en lecture et écriture à la base de données avec des privilèges administratifs limités pour certaines collections.

### Sécurité

Assurez-vous de ne pas exposer ces identifiants dans des environnements non sécurisés. Utilisez des variables d’environnement ou un gestionnaire de secrets pour des environnements de production.

## Configuration du Réseau

Un réseau Docker nommé `my_network` a été configuré pour connecter MongoDB et l'application Python. 

## Auteur

Ce projet a été réalisé par Maeva BEAUVILLAIN BERTE.  
N'hésitez pas à me contacter pour toute question ou suggestion concernant ce projet.  