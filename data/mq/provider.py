from pymongo import MongoClient
from collections import defaultdict
import numpy as np

dbname = 'belgium'
collection_name = 'pme'

def get_pme_ratios():
    client = MongoClient()
    db = client.get_database(dbname)
    collection = db[collection_name]
    cursor = collection.find()
    dico = defaultdict()
    for e in cursor:
        ratios_dico = defaultdict()
        ratios_dico["id"] = e["id"]
        ratios = ["r"+ str(i) for i in range(0,21)]
        for r in ratios:
            for y in ["n", "n1", "n2"]:
                ind = r+y
                ratios_dico[ind] = e[ind]
        #Add default data
        if "d_year" in e:
            ratios_dico["d_year"] = e["d_year"]
        dico[e["id"]] = ratios_dico
    return dico
    
def get_names():
    client = MongoClient()
    db = client.get_database(dbname)
    collection = db[collection_name]
    cursor = collection.find()
    dico = defaultdict()
    for e in cursor:
        dico[e["id"]] = e["name"]
    return dico
    
def get_all_enterprises(dico):
    answer = []
    for key in dico:
        answer.append(key)
    return answer

def get_non_default(dico):
    answer = []
    for key in dico:
        if not "d_year" in dico[key]:
            answer.append(key)
    return answer   
        
def get_default(dico, years):
    set_of_years = set(years)
    answer = []
    for key in dico:
        if "d_year" in dico[key] and dico[key]["d_year"] in set_of_years:
            answer.append(key)
    return answer
        
def get_ratios_data(dico, entreprises, indicators, year):
    X = np.zeros((len(entreprises), len(indicators)))
    Y = np.ones(len(entreprises))
    for i in range(0, len(entreprises)):
        for j in range(0, len(indicators)):
            X[i,j] = dico[entreprises[i]][indicators[j]+year]
        if "d_year" in dico[entreprises[i]]:
            Y[i] = -1
    return X, Y
