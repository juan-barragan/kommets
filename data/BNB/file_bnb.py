from collections import defaultdict
from pymongo import MongoClient
import tax_form
import datetime
import csv

# This function parses the signalectique file and returns two dictionaries, entreprise->type 
# entreprise->status defaulted_entreprise->year of default
def parse_signaletique(file_name, keep_these_defaulted_types):
    default_set = set(keep_these_defaulted_types)
    answer = defaultdict()
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the header
        for row in reader:
            dico_entreprise = defaultdict()
            code = int(row[0].strip())
            # National identifier
            dico_entreprise["code"] = row[1].strip()
            # Enterprise name
            dico_entreprise["name"] = row[2].strip()
            # forme forme juridique
            dico_entreprise["type"] = int(row[9].strip())
            dico_entreprise["sector"] = row[8].strip()
            # Situation juridique
            dico_entreprise["status"] = int(row[10].strip())
            if (dico_entreprise["status"] in default_set):
                d = datetime.datetime.strptime( row[11].strip(), "%m/%d/%Y" )
                dico_entreprise["d_year"] = d.year
            answer[code] = dico_entreprise
    return answer

def filter_bnb_file(all_entreprises_file, signalectique_file, keep_these_types, keep_these_status, keep_these_defaulted_types, keep_these_defaulted_years, output_file):
    set_of_types = set(keep_these_types)
    set_of_defaulted_years = set(keep_these_defaulted_years)
    set_of_defaulted_types = set(keep_these_defaulted_types)
    set_of_status = set(keep_these_status)
    entreprises_data = parse_signaletique(signalectique_file, keep_these_defaulted_types)
    answer = []
    with open(all_entreprises_file, 'r') as f:
        for line in f:
            # read the identifiant 
            id = int(line[0:9])
            # These are healty entreprises
            if (entreprises_data[id]["type"] in set_of_types and entreprises_data[id]["status"] in set_of_status):
                answer.append(line.strip());
            # print also the defaulted entreprises keeping the required years
            if (entreprises_data[id]["status"] in set_of_defaulted_types and entreprises_data[id]["d_year"] in set_of_defaulted_years):
                answer.append(line.strip());
    with open(output_file, 'w') as f:
        for line in answer:
            f.write(line)
            f.write("\n")
    
    
def fill_up_mongodb(file_name, file_signalectique, keep_these_defaulted_types):
    entreprises_data = parse_signaletique(file_signalectique, keep_these_defaulted_types)
    client = MongoClient()
    db = client.get_database('belgium')
    collection = db['balance_sheets']
    file = open(file_name, "r")
    first_line = "O"
    offset = 11
    data_block = 49
    # Write headers 
    num_line = 0
    while (first_line != ""):
        first_line = file.readline()
        # Check the number of accounting data, placed on the 150th character, 149 pithon, length 4
        if (first_line != ""):
            id = int(first_line[0:9])
            num_acc_values = int(first_line[149:153])
            second_line = file.readline()
            # This data contains the indicators
            t = tax_form.tax_form(num_acc_values, second_line)
            #TODO: Magic number 21 = num ratios in line
            t.add_ratios(21, first_line)
            json_data = t.get_json(entreprises_data)
            #print json_data
            collection.insert(json_data)
            first_line = second_line
            num_line += 1
            print "processing "+ str(num_line)
    file.close()

def create_pme_collection():
    client = MongoClient()
    db = client.get_database('belgium')
    collection = db['balance_sheets']
    pme_collection = db["pme"]
    cursor_ = collection.find({"9087n":{ "$gte":40}, "20/58n":{ "$lte":40000000}})
    for e in cursor_:
        pme_collection.insert(e)

def insert_activity_code(file_name):
    client = MongoClient()
    db = client.get_database('belgium')
    activity_codes = db["codes"]
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        next(reader, None)  # skip the header
        row = next(reader, None)
        dico_indet = defaultdict()
        code = row[0].strip()[0:2] #00000 code just keep two digits
        dico_indet["id"] = code
        dico_indet["fr"] = row[2].strip()
        dico_indet["en"] = row[4].strip()
        activity_codes.insert(dico_indet)
        for row in reader:
            dico_activity = defaultdict()
            code = row[0].strip()
            if len(code) == 2:
                dico_activity["id"] = code
                dico_activity["fr"] = row[2].strip()
                dico_activity["en"] = row[4].strip()
                activity_codes.insert(dico_activity)


