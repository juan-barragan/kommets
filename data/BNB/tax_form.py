from collections import defaultdict
import numpy as np

class tax_form:
    indicator_default_value = 0
    def __init__(self, n, line):
        offset = 11
        self.enterprise_id_ = int(line[0:9])
        self.dico_ = defaultdict()
        for i in range(0, n):
            position = offset + i*49
            code = line[position:position + 7].strip()            
            ammount_n_2 = float(line[position+7:position + 20])
            self.dico_[(code,"n2")] = ammount_n_2
            ammount_n_1 = float(line[position+21:position + 34])    
            self.dico_[(code,"n1")] = ammount_n_1
            ammount_n = float(line[position+35:position + 48])                
            self.dico_[(code,"n")] = ammount_n

    def parse_float(self, s):
        answer = self.indicator_default_value
        try:
            answer = float(s)
        except ValueError:
            pass
        return answer 


    # This is the first line n ratios = 21
    def add_ratios(self, n, line):
        offset = 161
        for i in range(0, n):
            position = offset + i*39
            r_n_2 = self.parse_float(line[position:position+13])
            self.dico_[("r"+str(i), "n2")] = r_n_2
            r_n_1 = self.parse_float(line[position+13:position+26])
            self.dico_[("r"+str(i), "n1")] = r_n_1
            r_n = self.parse_float(line[position+26:position+39])
            self.dico_[("r"+str(i), "n")] = r_n

    def get_indicator(self,i,year="n"):
        key = (i,year)
        if key in self.dico_:
            return self.dico_[key]
        return indicator_default_value
        
    def get_all_indicators(self, year="n"):
        return self.dico_
    
    def get_json(self, entreprise_data):
        answer = entreprise_data[self.enterprise_id_]
        answer["id"] = self.enterprise_id_
        for key in self.dico_:
            ind, year = key
            s = ind + year
            answer[s] = self.dico_[key]
        return answer
           
    def dump(self):
        print self.enterprise_id_
        for key in self.dico_:
            print key, self.dico_[key]            
