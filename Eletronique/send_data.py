import requests
import json

url = "http://192.168.78.89:8000/CICO/postRaspberry""

# Les données textuelles
data = {
    "donneTest": "test"
}

# La photo à envoyer
files = {
    'photo': open('/home/cico/Cat-In-Cat-Out/Eletronique/Pictures/test.jpg', 'rb')
}

# Effectuer la requête POST
response = requests.post(url, data=data, files=files)
print(response.text)
