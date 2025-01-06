# Projet de Migration vers MongoDB avec Docker

**Dernière mise à jour : 6 janvier 2025**

Ce projet consiste à migrer des données médicales à partir d'un fichier CSV vers une base de données MongoDB, tout en utilisant Docker pour une gestion efficace de l'environnement.

## Prérequis

Avant de commencer, assurez-vous que vous avez les outils suivants installés sur votre machine :

- [Docker](https://www.docker.com/get-started) : pour exécuter les conteneurs.
- [Git](https://git-scm.com/) : pour cloner le dépôt.

> **Note :** Poetry est déjà installé et utilisé dans le conteneur Docker. Vous n'avez pas besoin de l'installer localement.

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

## Remarque

- **Redémarrage Automatique** :
  - MongoDB redémarre automatiquement en cas de panne (`restart: always`).
  - Le service Python ne redémarre pas automatiquement pour éviter des exécutions redondantes.

## Configuration du Réseau

Un réseau Docker nommé `my_network` a été configuré pour connecter MongoDB et l'application Python. 

## Auteur

Ce projet a été réalisé par Maeva BEAUVILLAIN BERTE.  
N'hésitez pas à me contacter pour toute question ou suggestion concernant ce projet.  