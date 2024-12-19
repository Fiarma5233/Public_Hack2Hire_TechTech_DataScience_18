# Utiliser l'image officielle légère de Python.
# https://hub.docker.com/_/python
FROM python:3.11-slim

RUN pip install --upgrade pip

# Permettre l'affichage immédiat des instructions et messages de log dans les journaux de Knative
ENV PYTHONUNBUFFERED True

# Copier le code local dans l'image du conteneur.
# Définir le répertoire de travail dans le conteneur à /app
ENV APP_HOME /app
WORKDIR $APP_HOME



COPY . ./

# Installer les dépendances de production.
# Exécute pip install pour les packages spécifiés dans requirements.txt
#RUN pip install  --no-cache-dir -r requirements.txt
RUN pip install   -r requirements.txt

#RUN pip install scipy-1.14.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

#RUN pip install --no-cache-dir --no-deps -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org

EXPOSE 8000
# Exécuter le service web au démarrage du conteneur. Ici, nous utilisons le serveur web gunicorn,
# avec un processus worker et 8 threads.
# Pour des environnements avec plusieurs cœurs de CPU, augmentez le nombre de workers
# pour qu'il soit égal au nombre de cœurs disponibles.
# Le timeout est réglé sur 0 pour désactiver les timeouts des workers pour permettre à Cloud Run de gérer l'échelonnement des instances.
#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
#CMD [ "gunicorn", "Hack2Hire_TechTech_DataScience_18.main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD gunicorn --bind 0.0.0.0:8000 Hack2Hire_TechTech_DataScience_18.main:app
# CMD [ "gunicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD [ "gunicorn", "main:app", "--bind", "0.0.0.0:8000" ]



# #################################

# # Use python:3.11-bullseye for system dependencies (optional but recommended)
# FROM python:3.12.8-bookworm

# WORKDIR /app

# # Install system dependencies (important for SciPy)
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         build-essential \
#         gfortran \
#         libatlas-base-dev \
#         liblapack-dev \
#         libblas-dev \
#         python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# RUN pip install --upgrade pip

# # Permettre l'affichage immédiat des instructions et messages de log dans les journaux de Knative
# ENV PYTHONUNBUFFERED=1 

# # Copier le code local dans l'image du conteneur.
# # Définir le répertoire de travail dans le conteneur à /app
# ENV APP_HOME=/app
# WORKDIR $APP_HOME

# COPY . ./

# # Installer les dépendances de production.
# # Exécute pip install pour les packages spécifiés dans requirements.txt
# RUN pip install --no-cache-dir --no-deps -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org

# EXPOSE 8000

# CMD ["gunicorn", "Hack2Hire_TechTech_DataScience_18.main:app", "--host", "0.0.0.0", "--port", "8000"]