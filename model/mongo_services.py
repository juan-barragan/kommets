from pymongo import MongoClient
import re
                                        
def get_enterprises_starting_with(letter):
    client = MongoClient()
    db = client.get_database('belgium')
    collection = db['pme']
    r = re.compile(r"^" + letter, re.IGNORECASE) 
    cursor = collection.find({"name":r}, sort=[('name', 1)])
    answer = []
    for document in cursor:
        answer.append({"id": document["id"], "name": document["name"]})
    return answer
    
def get_enterprise_document(id):
    client = MongoClient()
    db = client.get_database('belgium')
    collection = db['pme']
    elem = collection.find_one({"id":id})
    sector_collection = db["codes"]  
    sector_id = elem['sector'][:2] 
    elem_sector = sector_collection.find_one({'id':sector_id})
    return {"sector": elem_sector['fr'], "elem":elem}
