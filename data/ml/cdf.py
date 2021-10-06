import numpy as np
from bisect import bisect_left

class CumulativeFunction:
        def __init__(self, values):
                self.values = np.copy(values)
                self.values.sort()
                self.population = len(self.values)
                
        def __call__(self, x):
                cursor = bisect_left(self.values,x)
                return float(cursor)/self.population
