import requests
import json


url = "http://192.168.43.11:8000/CICO/postRaspberry"
#url = "http://172.20.10.6:8000/CICO/postRaspberry"
def send_data(dictionnaire) :
    # Les données textuelles
    data = {
        "donneTest": "test"
    }

    # La photo à envoyer
    dictionnaire 

    #token et cookies
    headers = {'X-CSRFToken': 'votre_token_csrf'}
    cookies = {'csrftoken': 'votre_token_csrf'}
    # Effectuer la requête POST
    response = requests.post(url, data=data, dictionnaire=dictionnaire, headers=headers, cookies=cookies)
    print(response.text)
