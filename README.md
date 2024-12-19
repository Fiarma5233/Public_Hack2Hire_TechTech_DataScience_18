# Hack2Hire_TechTech_DataScience_18

1. Entrainemnt des models
2. Sauvegarde du model model le plus performant 
3. Conteneurisation
    -   Craton du fichier .dockerignore pour ignoer certains fichiers ou dossiers
    -   Creation du fichier Dockerfile qui contient les instructions  necessaires a la conteneurisation de l'application
    -   Creation de l'image docker de notre app: docker build -t hack2hire_techtech_datascience_18 .
    -   Lancer docker: docker run --name container_name -p 8000:8000 image_name
                    docker run --name credit_risK_prediction -p 8000:8000 hack2hire_techtech_datascience_18

4. Utilisation du model
   -    Apres avoir lancer l'image docker,
   -    Ouvrir un autre terminal
   -    Tester le model en utilisant le fichier test.py du dossier test
   -    Executer le fichier test.py qui contient des donnees rentrees aleatoirement (vous pouvez changer les valeurs )  pour  tester le model
