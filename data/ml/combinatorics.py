import itertools
from mq import provider
from collections import defaultdict
import numpy as np

def get_permutations(n):
    ratios = ['r' + str(i) for i in range(0,n)]
    result = []
    for i in range(1, len(ratios)+1):
        for s in itertools.combinations(ratios, i):
            result.append(",".join(s))
    return result
            
def write_permutations(n, file_name):
    with open(file_name, "w") as f:
        for s in get_permutations(n):
            f.write(s + "\n")

# Given a year n and a set of ratios, we will try to found a separable set of indicators for the
# defaulted and not defaulted enterprises.
# we are interested on the ratios for the previous year as default indicators
def get_upper(prov, indicators, year):
    d_year = provider.get_default(prov, [year])
    non_default = provider.get_non_default(prov)
    upper_set = set(non_default)
    # if year == 2015, we ask for biland data on n-1
    sdy = "n1"  # String Default Year
    sndy = "n1" # String Non Default Year
    if year == 2014:
        sndy = "n2"
    for i in range(0,len(indicators)):
        X_d, Y_d = provider.get_ratios_data(prov, d_year, [indicators[i]], sdy)
        X_n, Y_n = provider.get_ratios_data(prov, non_default, [indicators[i]], sndy)
        last_value = np.max(X_d)
        non_default_dico_values = defaultdict()
        for k in range(0, len(X_n)):
            non_default_dico_values[non_default[k]] = X_n[k]	
        remaining = set([e for e in non_default if non_default_dico_values[e] >= last_value])
        upper_set.intersection_update(remaining)
    
    return list(upper_set)
    
def format_upper(prov, indicators, year):
    upper = get_upper(prov, indicators.split(","), year)
    return ":".join([indicators, str(len(upper))])




        
