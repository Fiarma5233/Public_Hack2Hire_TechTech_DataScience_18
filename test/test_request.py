
import requests


# Url de base  de l'API
url_base = 'http://127.0.0.1:8082'

# Test  du endpoint d'accueil
response = requests.get(f"{url_base}/")
print("Response du endpoint d'accueil :", response.text)

# Donnees d'exemple pour la prediction
donnees_predire = {
    "Age": 28,
    "Sex": "Female",
    "Job": 3,
    "Housing": "rent",
    "SavingAccounts": "moderate",
    "CheckingAccount": "little",
    "CreditAmount": 178976,
    "Duration": 14,
    "Purpose": "business"
}

#Test du endpoint de prediction
response = requests.post(f'{url_base}/predire', json=donnees_predire)
print("Response du endpoint de prediction: ", response.text)