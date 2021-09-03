import random as randm
import json
json_ = json.load(open("resources/arts.json", encoding="utf8"))
artlist = [json_[item] for item in json_]

def get_art(art_name):
    for item in json_:
        if item == art_name:
            return str(json_[item])
    return str(randm.choice(artlist))
def rndm():
    return str(randm.choice(artlist))