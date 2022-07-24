# from django.test import TestCase

# Create your tests here.

import requests

url = "https://api.ultramsg.com/instance11652/messages/chat"

payload = "token=4y8zjxfihamgcbed&to=120363044079347538@g.us&body=Oscar is testing don't worry group&priority=1&referenceId="
headers = {'content-type': 'application/x-www-form-urlencoded'}

# https://chat.whatsapp.com/KLFK2A9woIDAJt5SJcIDdc

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)