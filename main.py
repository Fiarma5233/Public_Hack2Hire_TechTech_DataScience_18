

############## V3 proposition cha

# from pydantic import BaseModel
# import numpy as np
# import pandas as pd  # Manipulation des données
# import joblib  # Charger le modèle sauvegardé
# from flask import Flask, jsonify, request, render_template

# # Charger le modèle logistic depuis le disque
# modele = joblib.load('pipeline_modele_logistic_regression.pkl')

# # Définition du schéma des données d'entrée avec Pydantic
# class DonneesEntree(BaseModel):
#     Age: int
#     Sex: str
#     Job: int
#     Housing: str
#     SavingAccounts: str  # Mapping pour 'Saving accounts'
#     CheckingAccount: str  # Mapping pour 'Checking account'
#     CreditAmount: int  # Mapping pour 'Credit amount'
#     Duration: int
#     Purpose: str

# # Fonction pour mapper les colonnes de Pydantic vers celles du modèle (avec espaces)
# def mapper_noms_colonnes(donnees_dict):
#     mapping = {
#         "SavingAccounts": "Saving accounts",
#         "CheckingAccount": "Checking account",
#         "CreditAmount": "Credit amount"
#     }
#     donnees_mapees = {mapping.get(col, col): valeur for col, valeur in donnees_dict.items()}
#     return donnees_mapees

# # Création de l'instance de l'application Flask
# app = Flask(__name__)

# # Route d'accueil
# @app.route('/', methods=['GET'])
# def home():
#     return render_template('home.html')

# # Route de prédiction
# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Récupérer les données du formulaire
#         donnees_predire = {
#             "Age": int(request.form['Age']),
#             "Sex": request.form['Sex'],
#             "Job": int(request.form['Job']),
#             "Housing": request.form['Housing'],
#             "SavingAccounts": request.form['SavingAccounts'],
#             "CheckingAccount": request.form['CheckingAccount'],
#             "CreditAmount": int(request.form['CreditAmount']),
#             "Duration": int(request.form['Duration']),
#             "Purpose": request.form['Purpose']
#         }

#         # Validation avec Pydantic
#         donnees = DonneesEntree(**donnees_predire)

#         # Mapper les noms de colonnes sans espace vers ceux du modèle avec espaces
#         donnees_mapees = mapper_noms_colonnes(donnees.dict())

#         # Conversion en DataFrame
#         donnees_df = pd.DataFrame([donnees_mapees])

#         # Prédiction
#         predictions = modele.predict(donnees_df)
#         probabilites = modele.predict_proba(donnees_df)[:, 1]

#         # Compilation des résultats
#         resultats = donnees.dict()
#         resultats['prediction'] = int(predictions[0])
#         resultats['probabilite_risque_solde'] = probabilites[0]

#         return render_template('predictions.html', resultats=resultats)
#     except Exception as e:
#         return jsonify({"erreur": str(e)})

# # Point d'entrée
# if __name__ == "__main__":
#     app.run(debug=True, port=8082)

################# Today




# from pydantic import BaseModel
# import numpy as np
# import pandas as pd  # Manipulation des données
# import joblib  # Charger le modèle sauvegardé
# from flask import Flask, jsonify, request, render_template

# # Charger le modèle logistic depuis le disque
# modele = joblib.load('pipeline_modele_logistic_regression.pkl')

# # Définition du schéma des données d'entrée avec Pydantic
# class DonneesEntree(BaseModel):
#     Age: int
#     Sex: str
#     Job: int
#     Housing: str
#     SavingAccounts: str
#     CheckingAccount: str
#     CreditAmount: int
#     Duration: int
#     Purpose: str

# # Fonction pour mapper les colonnes de Pydantic vers celles du modèle (avec espaces)
# def mapper_noms_colonnes(donnees_dict):
#     mapping = {
#         "SavingAccounts": "Saving accounts",
#         "CheckingAccount": "Checking account",
#         "CreditAmount": "Credit amount"
#     }
#     donnees_mapees = {mapping.get(col, col): valeur for col, valeur in donnees_dict.items()}
#     return donnees_mapees

# # Création de l'instance de l'application Flask
# app = Flask(__name__)

# # Route d'accueil
# @app.route('/', methods=['GET'])
# def home():
#     return render_template('home.html')



# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Récupérer les données du formulaire
#         donnees_predire = {
#             "Age": int(request.form['Age']),
#             "Sex": request.form['Sex'],
#             "Job": int(request.form['Job']),
#             "Housing": request.form['Housing'],
#             "SavingAccounts": request.form['SavingAccounts'],
#             "CheckingAccount": request.form['CheckingAccount'],
#             "CreditAmount": int(request.form['CreditAmount']),
#             "Duration": int(request.form['Duration']),
#             "Purpose": request.form['Purpose']
#         }

#         # Validation avec Pydantic
#         donnees = DonneesEntree(**donnees_predire)

#         # Mapper les noms de colonnes sans espace vers ceux du modèle avec espaces
#         donnees_mapees = mapper_noms_colonnes(donnees.dict())

#         # Conversion en DataFrame
#         donnees_df = pd.DataFrame([donnees_mapees])

#         # Prédiction
#         predictions = modele.predict(donnees_df)
#         probabilites = modele.predict_proba(donnees_df)[:, 1]

#         # Compilation des résultats
#         resultats = donnees.dict()
#         resultats['prediction'] = int(predictions[0])
#         resultats['probabilite_risque_solde'] = probabilites[0]

#         return render_template('predictions.html', resultats=resultats)
    
#     except Exception as e:
#         # Si une erreur se produit, transmettre l'erreur à la vue
#         return render_template('home.html', erreur=str(e))

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     try:
#         # Récupérer le fichier soumis
#         fichier = request.files['file']
#         if fichier.filename == '':
#             return render_template('home.html', erreur="Aucun fichier n'a été soumis.")

#         # Déterminer le type de fichier (CSV ou Excel)
#         if fichier.filename.endswith('.csv'):
#             data = pd.read_csv(fichier)
#         elif fichier.filename.endswith('.xls'):
#             # Utiliser xlrd pour les fichiers .xls
#             data = pd.read_excel(fichier, engine='xlrd')
#         elif fichier.filename.endswith('.xlsx'):
#             # Utiliser openpyxl pour les fichiers .xlsx
#             data = pd.read_excel(fichier, engine='openpyxl')
#         else:
#             return render_template('home.html', erreur="Format de fichier non pris en charge. Utilisez un fichier CSV ou Excel.")

#         # Préparation des données pour le modèle
#         data_mapee = data.rename(columns=lambda x: mapper_noms_colonnes({x: x}).get(x, x))
#         predictions = modele.predict(data_mapee)
#         probabilites = modele.predict_proba(data_mapee)[:, 1]

#         # Ajouter les prédictions et probabilités aux résultats
#         data['Prediction'] = predictions
#         data['Probabilité'] = probabilites

#         # Retourner les résultats sous forme de tableau HTML
#         return render_template('batch_predictions.html', table=data.to_html(index=False, classes='table table-striped'))

#     except Exception as e:
#         # Si une erreur se produit, transmettre l'erreur à la vue
#         return render_template('home.html', erreur=str(e))


# # Point d'entrée
# if __name__ == "__main__":
#     app.run(debug=True, port=8082)










#############################


import sys
import os

# Ajouter le dossier 'modele' au sys.path
current_dir = os.getcwd()  # Cela donne le répertoire actuel du script
modele_path = os.path.join(current_dir, 'modele')  # Chemin vers le dossier 'modele'
sys.path.append(modele_path)  # Ajouter ce chemin à sys.path

# Maintenant, vous pouvez importer votre classe depuis 'outlier_clipper.py'
from modele.outlier_clipper import OutlierClipper

# Maintenant, vous pouvez importer votre classe depuis le fichier 'outlier_clipper.py'
#from outlier_clipper import OutlierClipper

# Testez l'importation
print("Classe OutlierClipper importée avec succès !")



##############################







from pydantic import BaseModel
import numpy as np
import pandas as pd  # Manipulation des données
import joblib  # Charger le modèle sauvegardé
from flask import Flask, jsonify, request, render_template
import xlrd

import sys
import os
import joblib

# Ajouter le dossier contenant `outlier_clipper.py` au chemin Python
#
# Importer la classe OutlierClipper
#from outlier_clipper import OutlierClipper

# Charger le modèle logistic depuis le disque
#modele = joblib.load('pipeline_modele_logistic_regression.pkl')
modele = joblib.load(os.path.join(os.getcwd(), 'pipeline_modele_logistic_regression.pkl'))


# Définition du schéma des données d'entrée avec Pydantic
class DonneesEntree(BaseModel):
    Age: int
    Sex: str
    Job: int
    Housing: str
    SavingAccounts: str
    CheckingAccount: str
    CreditAmount: int
    Duration: int
    Purpose: str

# Fonction pour mapper les colonnes de Pydantic vers celles du modèle (avec espaces)
def mapper_noms_colonnes(donnees_dict):
    mapping = {
        "SavingAccounts": "Saving accounts",
        "CheckingAccount": "Checking account",
        "CreditAmount": "Credit amount"
    }
    donnees_mapees = {mapping.get(col, col): valeur for col, valeur in donnees_dict.items()}
    return donnees_mapees

# Création de l'instance de l'application Flask
app = Flask(__name__)

# Route d'accueil
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer les données du formulaire
        donnees_predire = {
            "Age": int(request.form['Age']),
            "Sex": request.form['Sex'],
            "Job": int(request.form['Job']),
            "Housing": request.form['Housing'],
            "SavingAccounts": request.form['SavingAccounts'],
            "CheckingAccount": request.form['CheckingAccount'],
            "CreditAmount": int(request.form['CreditAmount']),
            "Duration": int(request.form['Duration']),
            "Purpose": request.form['Purpose']
        }

        # Validation avec Pydantic
        donnees = DonneesEntree(**donnees_predire)

        # Mapper les noms de colonnes sans espace vers ceux du modèle avec espaces
        donnees_mapees = mapper_noms_colonnes(donnees.dict())

        # Conversion en DataFrame
        donnees_df = pd.DataFrame([donnees_mapees])

        # Prédiction
        predictions = modele.predict(donnees_df)
        probabilites = modele.predict_proba(donnees_df)[:, 1]

        # Compilation des résultats
        resultats = donnees.dict()
        resultats['prediction'] = int(predictions[0])
        resultats['probabilite_risque_solde'] = probabilites[0]

        return render_template('predictions.html', resultats=resultats)
    
    except Exception as e:
        # Si une erreur se produit, transmettre l'erreur à la vue
        return render_template('home.html', erreur=str(e))

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Récupérer le fichier soumis
        fichier = request.files['file']
        if fichier.filename == '':
            return render_template('home.html', erreur="Aucun fichier n'a été soumis.")

        # Déterminer le type de fichier (CSV ou Excel)
        if fichier.filename.endswith('.csv'):
            data = pd.read_csv(fichier)
        # elif fichier.filename.endswith('.xls'):
        #     # Utiliser xlrd pour les fichiers .xls
        #     data = pd.read_excel(fichier, engine='xlrd')
        elif fichier.filename.endswith('.xlsx'):
            # Utiliser openpyxl pour les fichiers .xlsx
            data = pd.read_excel(fichier, engine='openpyxl')
        else:
            return render_template('home.html', erreur="Format de fichier non pris en charge. Utilisez un fichier CSV ou Excel.")

        # Préparation des données pour le modèle
        data_mapee = data.rename(columns=lambda x: mapper_noms_colonnes({x: x}).get(x, x))
        predictions = modele.predict(data_mapee)
        probabilites = modele.predict_proba(data_mapee)[:, 1]

        # Ajouter les prédictions et probabilités aux résultats
        data['Prediction'] = predictions
        data['Probabilité'] = probabilites

        # Retourner les résultats sous forme de tableau HTML
        return render_template('batch_predictions.html', table=data.to_html(index=False, classes='table table-striped'))

    except Exception as e:
        # Si une erreur se produit, transmettre l'erreur à la vue
        return render_template('home.html', erreur=str(e))


# Point d'entrée
if __name__ == "__main__":
    app.run(debug=True, port=8082)
