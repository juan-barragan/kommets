from mq import provider
from ml import combinatorics
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn import svm
from sklearn import preprocessing
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def pca_2D_logit(prov, healthy, h_year, default, d_year, ratios):
    X_d, Y_d = provider.get_ratios_data(prov, default, ratios, d_year)
    X_h, Y_h = provider.get_ratios_data(prov, healthy, ratios, h_year)
    X = np.append(X_d, X_h, axis=0)
    Y = np.append(Y_d, Y_h)
    pca = PCA(n_components=2)
    X_n = pca.fit_transform(X)
    nd = len(X_d)

    end = provider.get_non_default(prov)
    X_nd, _ = provider.get_ratios_data(prov, end, ratios, h_year)
    plt.scatter(X_n[nd:,0], X_n[nd:,1], c = "blue")
    plt.scatter(X_n[:nd,0], X_n[:nd,1], c = "red")
    clf = linear_model.LogisticRegression(C=1, fit_intercept=True)
    clf.fit(X_n,Y)
    t = np.linspace(min(X_n[:,0]), max(X_n[:,0]))
    y_t = (-clf.coef_[0][0]*t + clf.intercept_[0])/clf.coef_[0][1]
    plt.plot(t, y_t, c="black")
    plt.show()
    
def pca_2D_svm(prov, healthy, h_year, default, d_year, ratios):
    X_d, Y_d = provider.get_ratios_data(prov, default, ratios, d_year)
    X_h, Y_h = provider.get_ratios_data(prov, healthy, ratios, h_year)
    X = np.append(X_d, X_h, axis=0)
    Y = np.append(Y_d, Y_h)
    pca = PCA(n_components=2)
    X_n = pca.fit_transform(X)
    nd = len(X_d)
    plt.scatter(X_n[:nd,0], X_n[:nd,1], c = "red")
    plt.scatter(X_n[nd:,0], X_n[nd:,1], c = "blue")
    clf = svm.SVC(kernel='linear', C=1)
    clf.fit(X_n,Y)
    t = np.linspace(min(X_n[:,0]), max(X_n[:,0]))
    y_t = (-clf.coef_[0][0]*t + clf.intercept_[0])/clf.coef_[0][1]
    plt.plot(t, y_t, c="black")
    plt.show()    
    
def distributions(prov, ratios, d_year):
    E_d = provider.get_default(prov, [d_year])
    E_h = provider.get_non_default(prov)
    # if default year = 2015
    ynd_s = "n1"
    yd_s = "n1"
    if (d_year == 2014):
        ynd_s = "n2"
        
    for r in ratios:
        X_d, _ = provider.get_ratios_data(prov, E_d, [r], yd_s)
        X_h, _ = provider.get_ratios_data(prov, E_h, [r], ynd_s)
        plt.hist(X_h, bins=200)
        plt.scatter(X_d, -100*np.ones(len(X_d)), c="red")
        plt.show()
        plt.clf()
        plt.close()
        


