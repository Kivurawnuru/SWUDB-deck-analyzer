import requests

class Card:
    def __init__(self, cid, cname, ctype, ccost):
        self.id = cid
        self.name = cname
        self.type = ctype
        self.cost = ccost
# Done before noticing swu-db.com API. Left here if needed in future
def get_card_old(id):
    url = "https://swudb.com/card/"
    cid = id
    id = "/".join(id.split('_'))
    a = requests.get(url+id)
    cname = " ".join((a.text.split('title>')[1].split('\n')[1].split('|')[0]).split())
    ctype = (a.text.split('row pb-1')[1].split("span>")[1][:-2])
    ccost = " ".join(a.text.split('Cost')[1].split('\n')[1].split())
    return (Card(cid, cname, ctype,ccost))
def get_card(id,cards):
    for card in cards:
        if(card["Set"]==id.split('_')[0] and card["Number"] == id.split('_')[1]):
            return(card)
    return(None)
def get_all_cards():
    url = "https://api.swu-db.com/cards/sor"
    a = requests.get(url)
    cards = a.json()
    return(cards["data"])
