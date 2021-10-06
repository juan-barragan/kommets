from mq import provider
from ml import metrics, combinatorics
import numpy as np
from sklearn import linear_model
# coding: utf8

from sklearn import svm
from sklearn.decomposition import PCA

def dot_product(a, X):
    ne = X.shape[0]
    answer = np.zeros(ne)
    for i in range(0, ne):
        answer[i] = np.sum(a*X[i,:])
    return answer
   
def scores_logit(prov, healthy, h_year, default, d_year, ratios):
    X_d, Y_d = provider.get_ratios_data(prov, default, ratios, d_year)
    X_h, Y_h = provider.get_ratios_data(prov, healthy, ratios, h_year)
    X = np.append(X_d, X_h, axis=0)
    Y = np.append(Y_d, Y_h)
    clf = linear_model.LogisticRegression(C=1, fit_intercept=True)
    clf.fit(X,Y)
    E_nd = provider.get_non_default(prov)
    X_nd, Y_nd = provider.get_ratios_data(prov, E_nd, ratios, h_year)
    
    scores_nd = dot_product(clf.coef_, X_nd)
    scores_d = dot_product(clf.coef_, X_d)
    scores_all = np.append(scores_nd, scores_d)
    return scores_all

def metric_logit(prov, healthy, h_year, default, d_year, ratios):
    return metrics.S_measure(scores_logit(prov, healthy, h_year, default, d_year, ratios))
    
def format_metric(prov, healthy, h_year, default, d_year, ratios):
    return ratios + ":" + str(metric_logit(prov, healthy, h_year, default, d_year, ratios.split(",")))

def logistic(prov, healthy, h_year, default, d_year, ratios):
    X_d, Y_d = provider.get_ratios_data(prov, default, ratios, d_year)
    X_h, Y_h = provider.get_ratios_data(prov, healthy, ratios, h_year)
    X = np.append(X_d, X_h, axis=0)
    Y = np.append(Y_d, Y_h)    
    clf = linear_model.LogisticRegression(C=1, fit_intercept=True)
    clf.fit(X,Y)
    return clf
    
def scoring_logit(coef, healthy, h_year, default, d_year, ratios):
    E_nd = np.append(provider.get_non_default(prov), provider.get_default(prov, [2015]))
    X_nd, Y_nd = provider.get_ratios_data(prov, E_nd, ratios, h_year)
    X_d, Y_d = provider.get_ratios_data(prov, default, ratios, d_year)
    scores_nd = dot_product(coef, X_nd)
    scores_d = dot_product(coef, X_d)
    scores_all = np.append(scores_nd, scores_d)
    E = np.append(E_nd, default)
    Y = np.append(Y_nd, Y_d)
    for i in range(len(scores_all)):
        print E[i], scores_all[i], Y[i]
        
def scoring_logit_N_1(coef, prov, h_year, d_year, ratios):
    E_nd = provider.get_non_default(prov)
    E_d = provider.get_default(prov, [2015])
    X_nd, Y_nd = provider.get_ratios_data(prov, E_nd, ratios, h_year)
    X_d, Y_d = provider.get_ratios_data(prov, E_d, ratios, d_year)
    scores_nd = dot_product(coef, X_nd)
    scores_d = dot_product(coef, X_d)
    scores_all = np.append(scores_nd, scores_d)
    E = np.append(E_nd, E_d)
    Y = np.append(Y_nd, Y_d)
    print "2014"
    for i in range(len(scores_all)):
        print E[i], scores_all[i], Y[i]
                
        
#prov = provider.get_pme_ratios()
#r5 = ['r0', 'r3', 'r12', 'r13', 'r18']
#healthy = combinatorics.get_upper(prov, r5, 2014)
#default = provider.get_default(prov, [2014])
#r = "r3,r5,r8,r10,r13,r15,r16,r18,r19".split(",")
#clf = logistic(prov, healthy, "n2", default, "n1", r)
#print clf.coef_
#scoring_logit(clf.coef_, healthy, "n2", default, "n1", r)
#scoring_logit_N_1(clf.coef_, prov, "n1", "n1", r)

#names = provider.get_names()
#for key in names.keys():
#    print key, ":", names[key].encode('utf-8')
