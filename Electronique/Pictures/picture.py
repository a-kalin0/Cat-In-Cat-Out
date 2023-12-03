import requests

url = 'http://127.0.0.1:8000/'
files = {'file': open('/home/cico/Cat-In-Cat-Out/Electronique/Pictures/test0.jpg', 'rb')}

response = requests.post(url, files=files)
