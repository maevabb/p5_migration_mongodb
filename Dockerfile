
FROM python:3.13.0
WORKDIR /app

# Copie des fichiers pyproject.toml et poetry.lock
COPY pyproject.toml poetry.lock ./

# Installation de Poetry
RUN pip install poetry

# Installation des dépendances à l'aide de Poetry
RUN poetry install --no-dev --no-root

# Copie du reste du projet dans le conteneur
COPY . .

# Lancement du script
CMD ["poetry", "run", "python", "insert_data.py"]