#!/usr/bin/env python3
import json
import csv
import scrap_url
import sys
import argparse
from getpass import getpass
import get_card 

def import_json(file):
    f = open(file)
    data = json.load(f)
    return(data)

def import_from_json(data, url):
    cards = {}

    #ADD LEADER
    cards[data['leader']['id']] = data['leader']['count']

    #ADD BASE
    cards[data['base']['id']] = data['base']['count']
   
    #ADD DECK
    for row in data['deck']:
        cards[row['id']] = row['count']
    
    #ADD SIDEBOARD
    for row in data['sideboard']:
        try:
            if(cards[row['id']]!=0):
                cards[row['id']]+=int(row['count'])
        except:
            cards[row['id']] = int(row['count'])
    deck = Deck(data['metadata']['name'],data['metadata']['author'],cards,url)
    return(deck)


def print_deck(name):
    for id,val in name.items():
        print(id,val)


def import_from_csv(filename):
    file = open(filename,'r')
    data = csv.DictReader(file, delimiter=',')
    owned = {}
    for row in data:
        owned[row['Set']+"_"+row['CardNumber']]=row['Count']
    return(owned)

    
def import_own_cards(file):
    data = csv.DictReader(file.splitlines(), delimiter=',')
    owned = {}
    for row in data:
        owned[row['Set']+"_"+row['CardNumber']]=row['Count']
    return(owned)


def compare_decks(deck, owned):
    owned_cards = {}
    missing_cards = {}
    for card,value in deck.cards.items():
        try:
            if(owned[card]):
                if(value-int(owned[card])>0):
                    missing_cards[card]=value-int(owned[card])
                    #print("Missing {}: {} cards".format(card,value-int(owned[card])))
                    owned_cards[card] = value-int(owned[card])
                else:
                    #print("All {} cards!".format(card))
                    owned_cards[card] = value
        except:
            #print("Missing {}: {} cards".format(card,value))
            missing_cards[card]=value
    deck.add_missing(missing_cards)
    deck.add_owned(owned_cards)
    return(deck)

def get_number_of_cards(deck):
    cards = 0
    for card, value in deck.items():
        cards +=value
    return cards

class Deck:
    def __init__(self, name, author, cards, url):
        self.name = name
        self.author = author
        self.cards = cards
        self.missing_cards = {}
        self.owned_cards = {}
        self.url = url
    def add_missing(self,missing_cards):
        self.missing_cards = missing_cards
    def add_owned(self,owned_cards):
        self.owned_cards = owned_cards
def compare_single_deck(owned, url):
    id = url.split("/")[-1]
    deck = import_from_json(scrap_url.get_json(id),url)
    compared = compare_decks(deck,owned)
    cards = {}
    all_cards = get_card.get_all_cards()
    for key in compared.missing_cards:
        cards[key] = {"card": get_card.get_card(key,all_cards), "missing" : compared.missing_cards[key]}
    return cards
    #print("{} by {}: compatibilty: {:.0%}. URL: {}".format(compared.name, compared.author, get_number_of_cards(compared.owned_cards)/get_number_of_cards(compared.cards),compared.url))

#get_from_swudb
#if len(sys.argv) < 2:
#    sys.exit('Usage: {}'.format(sys.argv[0])) # TODO
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', help='How to get owned cards - online from swudb or from local file', choices=['online','local'],required=True)
parser.add_argument('-f', '--filename', help='Filename with local cards')
parser.add_argument('-u', '--username', help='SWUDB username',default=None)
parser.add_argument('-p', '--password', help='SWUDB password. Could be added later.', default=None)
parser.add_argument('--top', help='Compare your owned cards with top 100 decks from SWUDB. Result as percentage of owned card per each deck', action='store_true')
parser.add_argument('--compare', help='Compare your owned cards with selected deck from SWUDB. Result as list of owned/not owned cards', action='store_true')
parser.add_argument('--url', help='URL to SWUDB deck to compare')
args = parser.parse_args()
owned = None
if(args.mode=='local'):
    if(not args.filename):
        parser.error("mode local requires filename")
    owned = import_from_csv(args.filename)
    if(not owned):
        print("Error. Please check your file")
        sys.exit()
if args.compare and (args.url is None):
    parser.error("--compare requires --url")
if(args.mode=='online'):
    if(not args.username):
        username = input("Please enter SWUDB username: ")
    else:
        username = args.username
    if(not args.password):
        password = getpass('Please enter SWUDB password for user {}: '.format(username))
    else:
        password = args.password
    owned_cards = scrap_url.get_own_cards(username, password)
    if(not owned_cards):
        print("Problem with login to SWUDB. Please check connection and/or username and password")
        sys.exit()
    owned = import_own_cards(owned_cards)
if(args.compare):
    cards = compare_single_deck(owned,args.url)
    print("Number, Cost, Name, Type, Rarity, Missing")
    for card in cards:
        # If needed, we can add other fields from list below
        #{'card': {'Set': 'SOR', 'Number': '230', 'Name': 'General Veers', 'Subtitle': 'Blizzard Force Commander', 'Type': 'Unit', 'Aspects': ['Villainy'], 'Traits': ['IMPERIAL', 'OFFICIAL'], 'Arenas': ['Ground'], 'Cost': '3', 'Power': '3', 'HP': '3', 'FrontText': 'Other friendly IMPERIAL units get +1/+1.', 'DoubleSided': False, 'Rarity': 'Uncommon', 'Unique': True, 'Artist': 'Steve Morris', 'FrontArt': 'https://d3alac64utt23z.cloudfront.net/images/cards/SOR/230.png', 'VariantType': 'Normal', 'MarketPrice': '0.21'}, 'missing': 1}
        try:
            print("{}, {}, {}, {}, {}, Missing: {}".format(cards[card]['card']["Number"], cards[card]['card']["Cost"], cards[card]['card']["Name"], cards[card]['card']["Type"], cards[card]['card']['Rarity'],cards[card]["missing"]))
        except: 
            print("{}, {}, {}, {}, {}, Missing: {}".format(cards[card]['card']["Number"], "N/A", cards[card]['card']["Name"], cards[card]['card']["Type"], cards[card]['card']['Rarity'],cards[card]["missing"]))

if(args.top):
    url = "https://swudb.com/decks/hot?Skip="
    ids = scrap_url.get_top_100(url)
    decks = {}
    sorted_list = {}
    done = 0
    for id in ids:
        decks[id] = import_from_json(scrap_url.get_json(id),"https://swudb.com/deck/view/"+id)
        decks[id] = compare_decks(decks[id],owned)
        sorted_list[id]=get_number_of_cards(decks[id].owned_cards)/get_number_of_cards(decks[id].cards)
        done+=1
        print("Verified: {}/{}".format(done,len(ids)),end='\r')
    # Print sorted list
    for id, key in sorted(sorted_list.items(), key=lambda p:p[1], reverse=True):
        print("{} by {}: compatibilty: {:.0%}. URL: {}".format(decks[id].name, decks[id].author, get_number_of_cards(decks[id].owned_cards)/get_number_of_cards(decks[id].cards),decks[id].url))
        

# TODO:
# refractor
# export to csv
