# coding: utf8

from BNB import tax_form
from BNB import file_bnb

#filter the whole file we retain only the real enterprises, real defaults starting on 2006
# file contaning the whole data of enterprises
all_name = "./raw/all.txt"
# output file for the first filtered 
filtered_name = "./raw/filtered.txt"
signaletique_name = "./raw/signalectique.csv"
codes_file = "./raw/codes_activites.csv"

# see cdrom_bnb.xls
enterprise_types = [1, # Société coopérative européenne
    6,  # Société coopérative à responsabilité illimitée
    8,  # Société coopérative à responsabilité limitée
    9,  # Coopérative à responsabilité limitée, coopérative de participation
    10, # Société privée à responsabilité limitée
    11, # Société en nom collecif
    12, # Société en commandité simple
    13, # Société en commandité par actions
    14, # Société anonyme
    15, # Société privée à responsabilité limitée
    21, # Société d'assurance mutuelle de droit privé
    25, # Société agricole
    27, # Societée Européenne
    60, # Groupement d'intérêt économique avec un siège en Belgique
    65] # Groupement Européen d'intérêt économique avec un siège en Belgique

enterprise_status = [0] # Situation juridique normale see cdrom_bnb.xls file
default_types = [50, # Faillite (ouverture)
    51, # Clôture de faillite en cas d'excusabilité
    52] # Clôture de faillite sans excusabilité du faillite
    
default_years = [2015,2014,2013,2012,2011,2010,2009,2008,2007,2006]

file_bnb.filter_bnb_file(all_name, signaletique_name, enterprise_types, enterprise_status, default_types, default_years, filtered_name)
file_bnb.fill_up_mongodb(filtered_name, signaletique_name, default_types)
file_bnb.create_pme_collection()
file_bnb.insert_activity_code(codes_file)
