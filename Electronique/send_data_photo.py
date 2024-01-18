import requests
import uuid

# URL de l'API
url = "https://cico.ovh:443/CICO/postRaspberry"

# Identifiant de l'appareil
deviceId = 1

def send_data(photo):
    # Token et cookies
    headers = {'X-CSRFToken': uuid.uuid1() }
    cookies = {'csrftoken': uuid.uuid1() }
    # Effectuer la requête POST
    response = requests.post(url, data={"deviceId": deviceId}, files=photo, headers=headers, cookies=cookies, verify=True)
    print(response.text)

# Chemin de l'image
image_path = 'livre.JPG'  

# Ouvrir l'image et l'envoyer
with open(image_path, 'rb') as image_file:
    image_data = {'image': image_file}
    send_data(image_data)
