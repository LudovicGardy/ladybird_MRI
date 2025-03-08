# Utiliser une image Python compatible
FROM python:3.13-rc-slim

# Définir le dossier de travail
WORKDIR /app

# Installer Poetry correctement (avec curl)
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copier les fichiers de configuration de Poetry
COPY pyproject.toml poetry.lock ./

# Installer les dépendances sans installer le projet lui-même
RUN poetry install --no-interaction --no-ansi --no-root

# Copier le reste du code de l'application
COPY . .

# Exposer le port de Streamlit
EXPOSE 8501

# Lancer l'application
CMD ["poetry", "run", "streamlit", "run", "main_web.py", "--server.port=8501", "--server.address=0.0.0.0"]
