# -*- coding: utf-8 -*-
import datetime
from collections import defaultdict
import json

def get_dates(elem):
    dates = ["2013-1-1", "2014-1-1", "2015-1-1"]
    if "d_year" in elem:
        last_year = int(elem["d_year"]);
        for i in range(0,len(dates)):
            dates[i] = str(last_year-len(dates)+i)+"-1-1";
    for i in range(0,len(dates)):
        dates[i] = int(datetime.datetime.strptime(dates[i], '%Y-%m-%d').strftime("%s"))*1000;
    return dates;

def get_years():
    return ["n2", "n1", "n"]

def dflt(elem, key):
    if not key in elem:
        return 0
    return elem[key]
    
def get_assets(elem):
    dates = get_dates(elem)
    years = get_years()
    actif_accounting_items = ('20/28', '29', '30/36', '40/41', '50/53')
    actif_accounting_names = ('Act immo', 'Créances LT', 'Stocks', 'Créances CT', 'tréso')           
    actif_data = []
    for i in range(0,len(actif_accounting_items)):
        ats = [];                         
        for j in range(0, len(years)):
            key = actif_accounting_items[i] + years[j] 
            ats.append({'x':dates[j], 'y':dflt(elem,key)})

        actif_data.append({'key':actif_accounting_names[i], 'values':ats});
    other_actif = [];
    other_actif.append({'x':dates[0], 
            'y':dflt(elem, "20/58n2") 
                - dflt(elem, "20/28n2") - dflt(elem, "29n2") - dflt(elem, "30/36n2") 
                - dflt(elem, "40/41n2") - dflt(elem, "50/53n2")}) 
             
    other_actif.append({'x':dates[0], 
            'y':dflt(elem, "20/58n1") 
                - dflt(elem, "20/28n1") - dflt(elem, "29n1") - dflt(elem, "30/36n1") 
                - dflt(elem, "40/41n1") - dflt(elem, "50/53n1")})
                
    other_actif.append({'x':dates[0], 
            'y':dflt(elem, "20/58n") 
                - dflt(elem, "20/28n") - dflt(elem, "29n") - dflt(elem, "30/36n") 
                - dflt(elem, "40/41n2") - dflt(elem, "50/53n")})
                     
    actif_data.append({'key':"Autres", 'values':other_actif})                 
    return json.dumps(actif_data)
    
def get_liabilities(elem):
    dates = get_dates(elem)
    years = get_years();
    liabilities_accounting_items = ('10/15', '16', '17', '42/48')
    liabilities_accounting_names = ('Capitaux Propres', 'Provisions', 'Dettes LT', 'Dettes CT')
    liabilities_data = []
    for i in range(0,len(liabilities_accounting_items)):
    	ats = []                         
        for j in range(0, len(years)):
            key = liabilities_accounting_items[i] + years[j] 
            ats.append({'x':dates[j], 'y':dflt(elem, key)})            
        liabilities_data.append({'key':liabilities_accounting_names[i], 'values':ats})
        other_liabilities = [];
        other_liabilities.append({'x':dates[0], 'y':dflt(elem,"10/49n2") - dflt(elem,"10/15n2") - 
                dflt(elem,"16n2") - dflt(elem,"17n2") - dflt(elem,"42/48n2")})
        other_liabilities.append({'x':dates[1], 'y':dflt(elem,"10/49n1") - dflt(elem,"10/15n1") - 
                dflt(elem, "16n1") - dflt(elem,"17n1") - dflt(elem, "42/48n1")})
        other_liabilities.append({'x':dates[2], 'y':dflt(elem,"10/49n") - dflt(elem,"10/15n") - 
                dflt(elem,"16n") - dflt(elem,"17n") - dflt(elem,"42/48n")});        

	liabilities_data.append({'key':"Autres", 'values':other_liabilities})
    return json.dumps(liabilities_data);
        
def get_results_data(elem):
    dates = get_dates(elem)
    years = get_years()
    accounting_items = ('9904', 'r10')
    accounting_names = ("Bénéfice de l'exercice", 'Rentabilité brute')
    results_data = [];
    for i in range(0,len(accounting_items)):
        ats = []                         
        for j in range(0,len(years)):
            key = accounting_items[i]+years[j] 
            ats.append({'x':dates[j], 'y':dflt(elem, key)})
        results_data.append({'key':accounting_names[i], 'values':ats})

    return json.dumps(results_data);


def get_quantiles(elem):
    quantiles = [3,4,5,8,9,10,11,16,18]
    quantiles_names = [ "Valeur ajoutée par personne", "Valeur ajoutée / Immobilisations corporelles brutes",
                        "frais de personnel / Valeur ajoutée", "Rentabilité nette des capitaux propres après impôts",
                        "Cash-flow / Capitaux propres", "Rentabilité brute de l’actif total avant impôts sur charges des dettes",
                        "Rentabilité nette de l’actif total avant impôts et charges des dettes", "Nombre de jours de crédit clients sur chiffre d'affaires",
                        "Capitaux propres / Ensemble des moyens d’action"]
    values= []
    for i in range(0, len(quantiles)):
        key = "qr"+str(quantiles[i])
        values.append({ 'label':quantiles_names[i], 'value':elem[key]})
	rvalue = [];
    rvalue.append({'key':"Quantiles", 'values': values}) 
    return json.dumps(rvalue)
    
def get_qvalues(elem):
    quantiles = [3,4,5,8,9,10,11,16,18];
    values= [];
    for i in range(0,len(quantiles)):
        key = "r"+str(quantiles[i])+"n"
        values.append(elem[key])
    return json.dumps(values)

    
