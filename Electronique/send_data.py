import requests
import json


#url = "http://192.168.43.11:8000/CICO/postRaspberry"
url = "http://172.20.10.6:8000/CICO/postRaspberry"
def send_data(dictionnaire) :

    #token et cookies
    headers = {'X-CSRFToken': 'votre_token_csrf'}
    cookies = {'csrftoken': 'votre_token_csrf'}
    # Effectuer la requête POST
    # response = requests.post(url, data=data, files=dictionnaire, headers=headers, cookies=cookies)
    response = requests.post(url, files=dictionnaire, headers=headers, cookies=cookies)
    print(response.text)
