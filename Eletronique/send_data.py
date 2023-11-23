import requests
import json

url = "http://192.168.43.11:8000/CICO/postRaspberry"

# Les données textuelles
data = {
    "donneTest": "test"
}

# La photo à envoyer
files = {
    'photo': open('/home/cico/Cat-In-Cat-Out/Eletronique/Pictures/test.jpg', 'rb')
}

#token et cookies
headers = {'X-CSRFToken': 'votre_token_csrf'}
cookies = {'csrftoken': 'votre_token_csrf'}
# Effectuer la requête POST
response = requests.post(url, data=data, files=files, headers=headers, cookies=cookies)
print(response.text)
