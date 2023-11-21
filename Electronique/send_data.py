import requests
import json

url = "http://adresse_ip_du_serveur:port/api/endpoint"

# Les données textuelles
data = {
    "champ1": "valeur1",
    "champ2": "valeur2"
}

# La photo à envoyer
files = {
    'photo': open('/chemin/vers/la/photo.jpg', 'rb')
}

# Effectuer la requête POST
response = requests.post(url, data=data, files=files)
print(response.text)
