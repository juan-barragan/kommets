from ml import combinatorics
#from pyspark import SparkContext, SparkConf
from mq import provider
import scoring 
import csv 
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn import linear_model
import numpy as np
import seaborn as sns

def get_intersections(file_name):
    answer = []
    with open(file_name) as f:
        reader = csv.reader(f, delimiter = ":")
        for row in reader:
            ratios = row[0]
            if len(ratios.split(",")) > 1:
                answer.append(row[0].strip().split(","))
    return answer

def look_up_best_ratios(ratios, year, cores, perms, results_dir):
    prov = provider.get_pme_ratios()
    sc = SparkContext("local[*]", "metrics")
    ratios_dt = [",".join(r) for r in ratios]
    #data_set = sc.parallelize(combinatorics.get_permutations(perms), cores)
    data_set = sc.parallelize(ratios_dt, cores)
    default = provider.get_default(prov, [year])
    for r in ratios:    
        healthy = combinatorics.get_upper(prov, r, year)
        f = lambda indicators: scoring.format_metric(prov, healthy, "n2", default, "n1", indicators)
        results = data_set.map(f)
        results.saveAsTextFile("-".join(r) + results_dir)
    
def plot_roc_curve(separating_ratios, feature_ratios):
    prov = provider.get_pme_ratios()
    default = provider.get_default(prov, [2014])
    healthy = combinatorics.get_upper(prov, separating_ratios, 2014)
    X_d, Y_d = provider.get_ratios_data(prov, default, feature_ratios, "n1")
    X_h, Y_h = provider.get_ratios_data(prov, healthy, feature_ratios, "n2")
    X = np.append(X_d, X_h, axis=0)
    Y = np.append(Y_d, Y_h)
    clf = linear_model.LogisticRegression(C=1, fit_intercept=True)
    clf.fit(X,Y)
    print 'coefficients'
    print clf.coef_
    # apply these coefficients to the data of 2015
    default_2015 = provider.get_default(prov, [2015])
    X_d, Y_d = provider.get_ratios_data(prov, default_2015, feature_ratios, "n1")
    healthy_all = provider.get_non_default(prov)
    X_nd, Y_nd = provider.get_ratios_data(prov, healthy_all, feature_ratios, "n1")
    scores_d = scoring.dot_product(clf.coef_, X_d)
    scores_nd = scoring.dot_product(clf.coef_, X_nd)
    labels = np.append(Y_nd, Y_d)
    scores = np.append(scores_nd, scores_d)
    print 'scores,labels'
    for s,l in zip (scores, labels):
        print s,l
    
    x, y, _ = roc_curve(labels, scores)
    auc_value = auc(x, y)
    plt.figure()
    lw = 2
    plt.plot(x, y, color='darkorange',
            lw=lw, label='ROC curve (area = %0.3f)' % auc_value)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve')
    plt.legend(loc="lower right")
    plt.show()


#look_up_best_ratios(get_intersections("intersections.csv"), 2014, 32, 21, "mtx_single")
#print get_intersections("intersections.csv")
plot_roc_curve("r3,r7,r15".split(","), "r3,r8,r10,r11,r19".split(","))
