from pymongo import MongoClient
import json

cl = MongoClient('mongodb://Dhanvant:dhanvant143@cluster0-shard-00-00.wmg51.mongodb.net:27017,cluster0-shard-00-01.'
                 'wmg51.mongodb.net:27017,cluster0-shard-00-02.wmg51.mongodb.net:27017/Saul?ssl=true&replicaSet='
                 'atlas-6buhiz-shard-0&authSource=admin&retryWrites=true&w=majority')
db = cl["Saul"]
udat = db["Userdata"]


def dump(name, mail, pwd):
    with open('Data/files/user.json', 'r') as f:
        data = json.load(f)
    value = data.get(name)
    if value is None:
        data[name] = pwd
        with open('Data/files/user.json', 'w') as f:
            json.dump(data, f)
        udat.insert_one({'_id': name, 'mail': mail, 'pwd': pwd})
        return True
    return False


def check(name, pwd):
    try:
        get = udat.find_one({"_id": name})["pwd"]
        if get == pwd:
            return True
    except:
        pass
    return False
