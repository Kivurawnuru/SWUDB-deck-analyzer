import requests
import json
import re
def get_ids(url):
    x = requests.get(url)
    ids = []
    for line in x.text.split('\n'):
        if("/deck/view" in line):
            for word in line.split("\""):
                if("/deck/view" in word):
                    ids.append(word.split("/")[-1])
    return(list(dict.fromkeys(ids)))


def get_json(id):
    url = "https://swudb.com/Deck/GetJsonFile/"
    x= requests.get(url+id)
    return(x.json())
def get_top_100(url):
    ids = []
    for i in range(0,20,20):
        ids += get_ids(url+str(i))
    return(ids)
def get_token(x):
    token = None
    for line in x.text.split('\n'):
        if("htmx-config" in line):
            token = line
    token = json.loads(token.split('\'')[1])
    return(token['antiForgery']['requestToken'])
def login(username, password):
    url = "https://swudb.com/Account/Login"
    client = requests.session()
    x = client.get(url)
    token = get_token(x)
    if(token):
        data  = {'Input.Username': username, 'Input.Password' : password, '__RequestVerificationToken' : token}
        r = client.post(url, data=data)
        for line in r.text.split('\n'):
            if "Invalid login attempt." in line:
                return None
    else:
        return None
    return client
def get_own_cards(username, password):
    own_url = "https://swudb.com/collection/bulk?handler=CollectionCsv"
    session = login(username, password)
    if(session):
        own_cards = session.get(own_url)
        return(own_cards.text)
    return(None)

