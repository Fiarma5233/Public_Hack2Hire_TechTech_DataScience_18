from pydantic import BaseModel
import numpy as np
import pandas as pd  # pour la manipulation des données
import joblib  # pour charger le modèle sauvegardé
from flask import Flask, jsonify, request
from sklearn.preprocessing import LabelEncoder

# Charger le modèle logistic depuis le disque
modele = joblib.load('/home/ser3nity/Hack2Hire_TechTech_DataScience_18/modele_logistic_regression.pkl')

# Définition du schéma des données d'entrée avec Pydantic.
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

# Création de l'instance de l'application flask
app = Flask(__name__)

# Instancier un LabelEncoder pour encoder les variables catégorielles
label_encoder = LabelEncoder()

# Définition de la route racine qui retourne un message de bienvenue
@app.route('/', methods=['GET'])
def accueil():
    """Route de bienvenue"""
    return jsonify({"message" : "Bienvenue sur l'API de prediction du risque de solvabilité"})

# Définition de la route de prédiction du risque de solvabilité 
@app.route('/predire', methods=['POST'])
def predire():
    """Endpoint pour les prédictions en utilisant le modèle chargé
        Les données d'entrée sont validées et transformées en dataframe pour le traitement
    """
    if not request.json:
        return jsonify({"erreur": "Aucun JSON fourni"}), 400
    
    try:
        # Extraction et validation des données d'entrée en utilisant Pydantic
        donnees = DonneesEntree(**request.json)

        # Encodage des variables catégorielles
        donnees.Sex = label_encoder.fit_transform([donnees.Sex])[0]
        donnees.Housing = label_encoder.fit_transform([donnees.Housing])[0]
        donnees.SavingAccounts = label_encoder.fit_transform([donnees.SavingAccounts])[0]
        donnees.CheckingAccount = label_encoder.fit_transform([donnees.CheckingAccount])[0]
        donnees.Purpose = label_encoder.fit_transform([donnees.Purpose])[0]

        # Conversion des données en DataFrame
        donnees_df = pd.DataFrame([donnees.dict()])

        # Utilisation du modèle pour prédire et obtenir les probabilités
        predictions = modele.predict(donnees_df)
        probalilities = modele.predict_proba(donnees_df)[:, 1]  # Probabilités de la classe positive

        # Compilation des résultats dans un dictionnaire
        resultats = donnees.dict()
        resultats['prediction'] = int(predictions[0])
        resultats['probilite_risque_solde'] = probalilities[0]

        # Renvoi des résultats sous forme de JSON
        return jsonify({'resultats': resultats})
    
    except Exception as e:
        # Gestion des erreurs et renvoi d'un message d'erreur
        return jsonify({"erreur" : str(e)})


# Point d'entrée pour exécuter l'application
if __name__ == "__main__":
    app.run(debug=True, port=8082)
