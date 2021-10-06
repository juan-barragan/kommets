from ml import combinatorics
from pyspark import SparkContext, SparkConf
from mq import provider


def intersections(year, num_perms, cores, results_dir):
    prov = provider.get_pme_ratios()
    sc = SparkContext("local[*]", "intersections")
    data_set = sc.parallelize(combinatorics.get_permutations(21), cores)
    f = lambda indicators: combinatorics.format_upper(prov, indicators, year)
    results = data_set.map(f)
    results.saveAsTextFile(results_dir)
    
intersections(2014, 21, 38, "res")


