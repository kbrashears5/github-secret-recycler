#!/usr/bin/env python3

# imports
from base64 import b64encode
from nacl import encoding, public
import requests

# set parameters
USERNAME = "" # github username
TOKEN = "" # PAT with repo scope
SECRET_NAME = "" # name of the secret
SECRET_VALUE = "" # value of the secret

# encrypt function
def encrypt(publicKey: str, secretValue: str) -> str:
    publicKey = public.PublicKey(publicKey.encode("utf-8"), encoding.Base64Encoder())

    sealed_box = public.SealedBox(publicKey)

    encrypted = sealed_box.encrypt(secretValue.encode("utf-8"))

    return b64encode(encrypted).decode("utf-8")

# create headers object
headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json'
}

# get all repositories
repos_response = requests.get('https://api.github.com/users/' + USERNAME + '/repos', headers=headers, auth=(USERNAME, TOKEN))
repos = repos_response.json()

# loop through all repositories
for repo in repos:
    repoName = repo['full_name']
    print(repoName)

    publicKey_response = requests.get('https://api.github.com/repos/' + repoName + '/actions/secrets/public-key', headers=headers, auth=(USERNAME, TOKEN))
    key = publicKey_response.json()
    print(key)

    # create body
    encryptedValue = encrypt(key['key'], SECRET_VALUE)
    data = '{"key_id":"' + key['key_id'] + '","encrypted_value":"' + encryptedValue + '"}'
    print(data)
    
    # create or update the secret
    response = requests.put('https://api.github.com/repos/' + repoName + '/actions/secrets/' + SECRET_NAME, headers=headers, data=data, auth=(USERNAME, TOKEN))
    print(response.json())

    print(" ")