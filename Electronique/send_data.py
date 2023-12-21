import requests
import json

#url = "http://192.168.43.11:8000/CICO/postRaspberry"
url = "https://cico.ovh:443/CICO/postRaspberry"

deviceId = 1
def send_data(dictionnaire) :

    #token et cookies
    headers = {'X-CSRFToken': 'votre_token_csrf'}
    cookies = {'csrftoken': 'votre_token_csrf'}
    # response = requests.post(url, data=data, files=dictionnaire, headers=headers, cookies=cookies)
    response = requests.post(url, data={"deviceId": deviceId}, files=dictionnaire, headers=headers, cookies=cookies, verify=False)
    print(response.text)
