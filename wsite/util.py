import requests

def fetch(url):
    data = requests.get(url)
    args = data.json()
    return args