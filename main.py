
# from pydantic import BaseModel, Field
# import numpy as np
# import  pandas as pd # pour la  manipulation des donnees
# import joblib # pour charger le model sauvegarder
# from flask import Flask, jsonify, request

# # charger le model logistic depuis le disque
# #modele = joblib.load('/home/ser3nity/Hack2Hire_TechTech_DataScience_18/modele_logistic_regression.pkl')

# modele = joblib.load('/home/ser3nity/Hack2Hire_TechTech_DataScience_18/pipeline_modele_logistic_regression.pkl')


# # Definition du schema des donnees d'entree avec Pydantic.
# #Cela garantie que les  donnees recues correspondent aux attentes du model
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



# # Creation de l'instance de l'application flask
# app = Flask(__name__)

# # Definition de la route racine qui retourne un message bienvenue
# @app.route('/', methods=['GET'])
# def accueil():
#     """Route de bienvenue"""
#     return jsonify({"message" : "Bienvenue sur l'API de prediction du riste de solvabilite"})

# # Definition de la route de predicition du risque de solvabilite 
# @app.route('/predire', methods=['POST'])
# def predire():
#     """Endpoint pour les predictions en  utilisant le modele charge
#         Les donnees d'entree sont validees et transforees en dataframe pour le traitement

#     """

#     if not request.json:
#         return jsonify({"erreur": "Aucun JSON fourni"}), 400
    
#     try:
#         #Extracton et validation des donnees d'entree en utiisant Pydantic
#         donnees = DonneesEntree(**request.json)
#         donnees_df = pd.DataFrame([donnees.dict()]) # Conversion en Dataframe

#         #Utilisation du  modele pour predire et obtenir les probabilites
#         predictions = modele.predict(donnees_df)
#         probalilities = modele.predict_proba(donnees_df)[:,1] # Probabilites de la classe  positive

#         #Compilation des resultats dans un dicionnaire
#         resultats = donnees.dict()
#         resultats['prediction'] = int(predictions[0])
#         resultats['probilite_risque_solde'] = probalilities[0]

#         #Renvoi des resultats sous formre de json
#         return jsonify({'resultats': resultats})
    
#     except Exception as e:
#         # Gestion des erreur s et renvoi d'un message d'erreur
#         return jsonify({"erreur" : str(e)})


# #Point d'entreer pour executer l'application
# if __name__ == "__main__":
#     app.run(debug= True, port=8082)



######### V2 bien ################


# from pydantic import BaseModel
# import numpy as np
# import pandas as pd  # Manipulation des données
# import joblib  # Charger le modèle sauvegardé
# from flask import Flask, jsonify, request
# import os
# from joblib import load
# # Charger le modèle logistic depuis le disque
# #modele = joblib.load('/home/fiarma-landry-some/Hack2Hire_TechTech_DataScience_18/pipeline_modele_logistic_regression.pkl')

# modele = joblib.load('pipeline_modele_logistic_regression.pkl')

# ############
# # # Obtenir le répertoire actuel où se trouve main.py
# # current_dir = os.path.dirname(os.path.abspath(__file__))

# # # Construire un chemin dynamique vers le modèle
# # model_path = os.path.join(current_dir, 'modele', 'pipeline_modele_logistic_regression.pkl')

# # # Vérifier l'existence du fichier
# # if not os.path.exists(model_path):
# #     raise FileNotFoundError(f"Le fichier modèle n'existe pas à l'emplacement : {model_path}")

# # # Charger le modèle
# # modele = joblib.load(model_path)

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
#     # Retourner un dictionnaire avec les noms de colonnes adaptés
#     donnees_mapees = {mapping.get(col, col): valeur for col, valeur in donnees_dict.items()}
#     return donnees_mapees

# # Création de l'instance de l'application Flask
# app = Flask(__name__)

# # Route d'accueil
# @app.route('/', methods=['GET'])
# def accueil():
#     return jsonify({"message": "Bienvenue sur l'API de prédiction du risque de solvabilité"})

# # Route de prédiction
# @app.route('/predire', methods=['POST'])
# def predire():
#     if not request.json:
#         return jsonify({"erreur": "Aucun JSON fourni"}), 400

#     try:
#         # Validation avec Pydantic
#         donnees = DonneesEntree(**request.json)
        
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

#         return jsonify({'resultats': resultats})

#     except Exception as e:
#         return jsonify({"erreur": str(e)})

# # Point d'entrée
# if __name__ == "__main__":
#     app.run(debug=True, port=8082)


################ V3 en cours de developpement #


# from pydantic import BaseModel
# import numpy as np
# import pandas as pd  # Manipulation des données
# import joblib  # Charger le modèle sauvegardé
# from flask import Flask, jsonify, request, render_template
# import os
# from joblib import load
# # Charger le modèle logistic depuis le disque
# #modele = joblib.load('/home/fiarma-landry-some/Hack2Hire_TechTech_DataScience_18/pipeline_modele_logistic_regression.pkl')

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
#     # Retourner un dictionnaire avec les noms de colonnes adaptés
#     donnees_mapees = {mapping.get(col, col): valeur for col, valeur in donnees_dict.items()}
#     return donnees_mapees

# # Création de l'instance de l'application Flask
# app = Flask(__name__)

# # Route d'accueil
# @app.route('/', methods=['GET'])
# def accueil():
#     return render_template('home.html')

# # Route de prédiction
# @app.route('/predict', methods=['POST'])
# def home():
    
#     # #recuperer entrees dans le formulaire
#     # age = request.form['Age']
#     # sex = request.form['Sex']
#     # job = request.form['Job']
#     # housing = request.form['Housing']
#     # savingAccounts = request.form['SavingAccounts']
#     # checkingAccount = request.form['CheckingAccount']
#     # creditAmount = request.form['CreditAmount']
#     # duration = request.form['Duration']
#     # purpose = request.form['Purpose']

#     #recuperer entrees dans le formulaire
#     donnees_predire = {
#     "Age": request.form['Age'],
#     "Sex": request.form['Sex'],
#     "Job": request.form['Job'],
#     "Housing": request.form['Housing'],
#     "SavingAccounts": request.form['SavingAccounts'],
#     "CheckingAccount": request.form['CheckingAccount'],
#     "CreditAmount": request.form['CreditAmount'],
#     "Duration": request.form['Duration'],
#     "Purpose": request.form['Purpose']
#     }

#     try:
#         # Validation avec Pydantic
#         donnees = DonneesEntree(**request.json)
        
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


############## V3 proposition cha

from pydantic import BaseModel
import numpy as np
import pandas as pd  # Manipulation des données
import joblib  # Charger le modèle sauvegardé
from flask import Flask, jsonify, request, render_template

# Charger le modèle logistic depuis le disque
modele = joblib.load('pipeline_modele_logistic_regression.pkl')

# Définition du schéma des données d'entrée avec Pydantic
class DonneesEntree(BaseModel):
    Age: int
    Sex: str
    Job: int
    Housing: str
    SavingAccounts: str  # Mapping pour 'Saving accounts'
    CheckingAccount: str  # Mapping pour 'Checking account'
    CreditAmount: int  # Mapping pour 'Credit amount'
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

# Route de prédiction
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
        return jsonify({"erreur": str(e)})

# Point d'entrée
if __name__ == "__main__":
    app.run(debug=True, port=8082)
