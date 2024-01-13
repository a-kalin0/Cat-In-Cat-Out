import requests
import json

#url = "http://172.20.10.4:8000/CICO/postRaspberry"
url = "https://cico.ovh:443/CICO/postRaspberry"


deviceId = 1
def send_data(dictionnaire) :

    #token et cookies
    headers = {'X-CSRFToken': 'votre_token_csrf'}
    cookies = {'csrftoken': 'votre_token_csrf'}
    # Effectuer la requête POST
    # response = requests.post(url, data=data, files=dictionnaire, headers=headers, cookies=cookies)
    response = requests.post(url, data={"deviceId": deviceId}, files=dictionnaire, headers=headers, cookies=cookies, verify=True)
    #response = requests.post(url, data={"deviceId": deviceId}, files=dictionnaire, headers=headers, cookies=cookies)
    print(response.text)
