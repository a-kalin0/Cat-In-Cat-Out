import requests
import json

url = "http://192.168.15.98:8000/CICO/endpoint"

# Les données textuelles
data = {
    "champ1": "valeur1",
    "champ2": "valeur2"
}

# La photo à envoyer
#files = {
#    'photo': open('/chemin/vers/la/photo.jpg', 'rb')
}

# Effectuer la requête POST
#response = requests.post(url, data=data, files=files)
response = requests.post(url, data=data)
print(response.text)
