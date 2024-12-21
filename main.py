
# import os
# import io
# import sys
# import pandas as pd
# from flask import Flask, jsonify, request, render_template, send_file
# from pydantic import BaseModel
# from joblib import load

# import sys
# import os

# # Ajouter le dossier 'modele' au sys.path
# current_dir = os.getcwd()  # Cela donne le répertoire actuel du script
# modele_path = os.path.join(current_dir, 'modele')  # Chemin vers le dossier 'modele'
# sys.path.append(modele_path)  # Ajouter ce chemin à sys.path

# # Maintenant, vous pouvez importer votre classe depuis 'outlier_clipper.py'
# #from modele.outlier_clipper import OutlierClipper

# import sys


# #Maintenant, vous pouvez importer votre classe depuis le fichier 'outlier_clipper.py'
# from modele.outlier_clipper import OutlierClipper

# # Testez l'importation
# print("Classe OutlierClipper importée avec succès !")


# from pydantic import BaseModel
# import numpy as np
# import pandas as pd  # Manipulation des données
# import joblib  # Charger le modèle sauvegardé
# from flask import Flask, jsonify, request, render_template
# import xlrd

# import sys
# import os
# import joblib


# # Charger le modèle logistic depuis le disque
# modele = joblib.load('pipeline_modele_logistic_regression.jolib')

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

# # Route pour effectuer une prédiction individuelle
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

# # Route pour effectuer des prédictions en batch et permettre le téléchargement
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

#         # Sauvegarder les résultats temporairement pour téléchargement
#         global batch_results
#         batch_results = data

#         # Retourner les résultats sous forme de tableau HTML
#         return render_template('batch_predictions.html', table=data.to_html(index=False, classes='table table-striped'))

#     except Exception as e:
#         # Si une erreur se produit, transmettre l'erreur à la vue
#         return render_template('home.html', erreur=str(e))

# # Route pour télécharger les résultats en batch
# @app.route('/download', methods=['POST'])
# def download_file():
#     try:
#         # Vérifier si les résultats sont disponibles
#         if 'batch_results' not in globals() or batch_results is None:
#             return render_template('home.html', erreur="Aucun résultat à télécharger.")

#         # Choix du format de téléchargement
#         format_choisi = request.form['format']
#         output = io.BytesIO()

#         if format_choisi == 'csv':
#             batch_results.to_csv(output, index=False)
#             output.seek(0)
#             return send_file(output, as_attachment=True, download_name='predictions.csv', mimetype='text/csv')

#         elif format_choisi == 'xlsx':
#             with pd.ExcelWriter(output, engine='openpyxl') as writer:
#                 batch_results.to_excel(writer, index=False)
#             output.seek(0)
#             return send_file(output, as_attachment=True, download_name='predictions.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

#         else:
#             return render_template('home.html', erreur="Format de téléchargement non pris en charge.")

#     except Exception as e:
#         return render_template('home.html', erreur=str(e))

# # Point d'entrée
# if __name__ == "__main__":
#     app.run(debug=True, port=8082)

######################Version bien #################

# import os
# import io
# import sys
# import pandas as pd
# from flask import Flask, jsonify, request, render_template, send_file
# from pydantic import BaseModel
# from joblib import load
# from weasyprint import HTML
# import tempfile

# # Ajouter le dossier 'modele' au sys.path
# current_dir = os.getcwd()
# modele_path = os.path.join(current_dir, 'modele')
# sys.path.append(modele_path)

# from modele.outlier_clipper import OutlierClipper

# # Charger le modèle logistic depuis le disque
# modele = load('pipeline_modele_logistic_regression.jolib')

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

# # Route pour effectuer une prédiction individuelle
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
#         return render_template('home.html', erreur=str(e))

# # Route pour télécharger les résultats sous forme de PDF
# @app.route('/download-pdf', methods=['POST'])
# def download_pdf():
#     try:
#         # Récupérer les résultats à inclure dans le PDF
#         resultats = request.form.to_dict()

#         # Utiliser un template HTML pour générer le PDF
#         html = render_template('predictions.html', resultats=resultats)

#         # Créer un fichier PDF temporaire
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
#             HTML(string=html).write_pdf(temp_pdf.name)
#             temp_pdf.seek(0)
#             return send_file(temp_pdf.name, as_attachment=True, download_name='resultats.pdf', mimetype='application/pdf')

#     except Exception as e:
#         return render_template('home.html', erreur=f"Erreur lors de la génération du PDF: {str(e)}")

# # Point d'entrée
# if __name__ == "__main__":
#     app.run(debug=True, port=8082)


######################

# import os
# import io
# import sys
# import pandas as pd
# from flask import Flask, jsonify, request, render_template, send_file
# from pydantic import BaseModel
# from joblib import load

# import sys
# import os

# # Ajouter le dossier 'modele' au sys.path
# current_dir = os.getcwd()  # Cela donne le répertoire actuel du script
# modele_path = os.path.join(current_dir, 'modele')  # Chemin vers le dossier 'modele'
# sys.path.append(modele_path)  # Ajouter ce chemin à sys.path

# # Maintenant, vous pouvez importer votre classe depuis 'outlier_clipper.py'
# #from modele.outlier_clipper import OutlierClipper

# import sys


# #Maintenant, vous pouvez importer votre classe depuis le fichier 'outlier_clipper.py'
# from modele.outlier_clipper import OutlierClipper

# # Testez l'importation
# print("Classe OutlierClipper importée avec succès !")


# from pydantic import BaseModel
# import numpy as np
# import pandas as pd  # Manipulation des données
# import joblib  # Charger le modèle sauvegardé
# from flask import Flask, jsonify, request, render_template
# import xlrd

# import sys
# import os
# import joblib


# # Charger le modèle logistic depuis le disque
# modele = joblib.load('pipeline_modele_logistic_regression.jolib')

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

# # Route pour effectuer une prédiction individuelle
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

# # Route pour effectuer des prédictions en batch et permettre le téléchargement
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

#         # Sauvegarder les résultats temporairement pour téléchargement
#         global batch_results
#         batch_results = data

#         # Retourner les résultats sous forme de tableau HTML
#         return render_template('batch_predictions.html', table=data.to_html(index=False, classes='table table-striped'))

#     except Exception as e:
#         # Si une erreur se produit, transmettre l'erreur à la vue
#         return render_template('home.html', erreur=str(e))

# # Route pour télécharger les résultats en batch
# @app.route('/download', methods=['POST'])
# def download_file():
#     try:
#         # Vérifier si les résultats sont disponibles
#         if 'batch_results' not in globals() or batch_results is None:
#             return render_template('home.html', erreur="Aucun résultat à télécharger.")

#         # Choix du format de téléchargement
#         format_choisi = request.form['format']
#         output = io.BytesIO()

#         if format_choisi == 'csv':
#             batch_results.to_csv(output, index=False)
#             output.seek(0)
#             return send_file(output, as_attachment=True, download_name='predictions.csv', mimetype='text/csv')

#         elif format_choisi == 'xlsx':
#             with pd.ExcelWriter(output, engine='openpyxl') as writer:
#                 batch_results.to_excel(writer, index=False)
#             output.seek(0)
#             return send_file(output, as_attachment=True, download_name='predictions.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

#         else:
#             return render_template('home.html', erreur="Format de téléchargement non pris en charge.")

#     except Exception as e:
#         return render_template('home.html', erreur=str(e))

# # Route pour télécharger les résultats sous forme de PDF
# from weasyprint import HTML
# import tempfile


# from weasyprint import HTML
# import tempfile


# @app.route('/download-pdf', methods=['POST'])
# def download_pdf():
#     try:
#         # Récupérer les résultats pour la page de prédiction
#         resultats = request.form.to_dict()

#         # Convertir les valeurs numériques (comme la probabilité) en float
#         if 'probabilite_risque_solde' in resultats:
#             resultats['probabilite_risque_solde'] = float(resultats['probabilite_risque_solde'])
        
#         # Convertir la prédiction en entier
#         if 'prediction' in resultats:
#             resultats['prediction'] = int(resultats['prediction'])

#         # Générer le contenu HTML de la page avec les résultats de la prédiction (sans le bouton)
#         html_content = render_template('predictions_pdf.html', resultats=resultats)

#         # Créer un fichier PDF temporaire
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
#             HTML(string=html_content).write_pdf(temp_pdf.name)
#             temp_pdf.seek(0)
#             return send_file(temp_pdf.name, as_attachment=True, download_name='resultats.pdf', mimetype='application/pdf')

#     except Exception as e:
#         return render_template('home.html', erreur=f"Erreur lors de la génération du PDF: {str(e)}")

# # Point d'entrée
# if __name__ == "__main__":
#     app.run(debug=True, port=8082)


import os
import io
import sys
import pandas as pd
from flask import Flask, jsonify, request, render_template, send_file, session
from pydantic import BaseModel
from joblib import load
import tempfile, joblib
from weasyprint import HTML

# Ajouter le dossier 'modele' au sys.path
current_dir = os.getcwd()  # Cela donne le répertoire actuel du script
modele_path = os.path.join(current_dir, 'modele')  # Chemin vers le dossier 'modele'
sys.path.append(modele_path)  # Ajouter ce chemin à sys.path

# Importation du modèle et de la classe
from modele.outlier_clipper import OutlierClipper

# Charger le modèle logistic depuis le disque
modele = joblib.load('pipeline_modele_logistic_regression.jolib')

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
app.secret_key = 'votre_clé_secrète'  # Définissez une clé secrète pour la session

# Route d'accueil
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# Route pour effectuer une prédiction individuelle
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

        # Sauvegarder les résultats dans la session
        session['resultats'] = resultats

        # Envoyer les résultats au template
        return render_template('predictions.html', resultats=resultats)
    
    except Exception as e:
        # Si une erreur se produit, transmettre l'erreur à la vue
        return render_template('home.html', erreur=str(e))

# Route pour effectuer des prédictions en batch et permettre le téléchargement
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
        elif fichier.filename.endswith('.xlsx'):
            # Utiliser openpyxl pour les fichiers .xlsx
            data = pd.read_excel(fichier, engine='openpyxl')
        else:
            return render_template('home.html', erreur="Format de fichier non pris en charge. Utilisez un fichier CSV ou xlsx.")

        # Préparation des données pour le modèle
        data_mapee = data.rename(columns=lambda x: mapper_noms_colonnes({x: x}).get(x, x))
        predictions = modele.predict(data_mapee)
        probabilites = modele.predict_proba(data_mapee)[:, 1]

        # Ajouter les prédictions et probabilités aux résultats
        data['Prediction'] = predictions
        data['Probabilité'] = probabilites

        # Sauvegarder les résultats temporairement pour téléchargement
        global batch_results
        batch_results = data

        # Retourner les résultats sous forme de tableau HTML
        return render_template('batch_predictions.html', table=data.to_html(index=False, classes='table table-striped'))

    except Exception as e:
        # Si une erreur se produit, transmettre l'erreur à la vue
        return render_template('home.html', erreur=str(e))
    
     # Route pour télécharger les résultats en batch
@app.route('/download', methods=['POST'])
def download_file():
    try:
        # Vérifier si les résultats sont disponibles
        if 'batch_results' not in globals() or batch_results is None:
            return render_template('home.html', erreur="Aucun résultat à télécharger.")

        # Choix du format de téléchargement
        format_choisi = request.form['format']
        output = io.BytesIO()

        if format_choisi == 'csv':
            batch_results.to_csv(output, index=False)
            output.seek(0)
            return send_file(output, as_attachment=True, download_name='predictions.csv', mimetype='text/csv')

        elif format_choisi == 'xlsx':
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                batch_results.to_excel(writer, index=False)
            output.seek(0)
            return send_file(output, as_attachment=True, download_name='predictions.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        else:
            return render_template('home.html', erreur="Format de téléchargement non pris en charge.")

    except Exception as e:
        return render_template('home.html', erreur=str(e))

# # Route pour télécharger les résultats sous forme de PDF
# @app.route('/download-pdf', methods=['POST'])
# def download_pdf():
#     try:
#         # Vérifier si les résultats sont dans la session
#         if 'resultats' not in session:
#             return render_template('home.html', erreur="Les résultats de la prédiction sont manquants.")

#         # Récupérer les résultats depuis la session
#         resultats = session['resultats']

#         # Convertir les valeurs numériques (comme la probabilité) en float
#         resultats['probabilite_risque_solde'] = float(resultats['probabilite_risque_solde'])
#         resultats['prediction'] = int(resultats['prediction'])

#         ##Récupérer les résultats pour la page de prédiction
# #       #resultats .to_dict()

#         # Générer le contenu HTML de la page avec les résultats de la prédiction (sans le bouton)
#         html_content = render_template('predictions_pdf.html', resultats=resultats)

#         # Créer un fichier PDF temporaire
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
#             HTML(string=html_content).write_pdf(temp_pdf.name)
#             temp_pdf.seek(0)
#             return send_file(temp_pdf.name, as_attachment=True, download_name='resultats.pdf', mimetype='application/pdf')

#     except Exception as e:
#         return render_template('home.html', erreur=f"Erreur lors de la génération du PDF: {str(e)}")


@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    try:
        # Vérifier si les résultats sont dans la session
        if 'resultats' not in session:
            return render_template('home.html', erreur="Les résultats de la prédiction sont manquants.")

        # Récupérer les résultats depuis la session
        resultats = session['resultats']

        # Tri explicite des résultats pour garantir l'ordre dans le PDF
        order = [
            'Age', 'Sex', 'Job', 'Housing', 'SavingAccounts', 
            'CheckingAccount', 'CreditAmount', 'Duration', 'Purpose', 
            'prediction', 'probabilite_risque_solde'
        ]

        # Créer un dictionnaire trié
        resultats_sorted = {key: resultats[key] for key in order}

        # Convertir les valeurs numériques (comme la probabilité) en float
        resultats_sorted['probabilite_risque_solde'] = float(resultats_sorted['probabilite_risque_solde'])
        resultats_sorted['prediction'] = int(resultats_sorted['prediction'])

        # Générer le contenu HTML de la page avec les résultats triés
        html_content = render_template('predictions_pdf.html', resultats=resultats_sorted)

        # Créer un fichier PDF temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            HTML(string=html_content).write_pdf(temp_pdf.name)
            temp_pdf.seek(0)
            return send_file(temp_pdf.name, as_attachment=True, download_name='resultats.pdf', mimetype='application/pdf')

    except Exception as e:
        return render_template('home.html', erreur=f"Erreur lors de la génération du PDF: {str(e)}")

# Point d'entrée
if __name__ == "__main__":
    app.run(debug=True, port=8082)
