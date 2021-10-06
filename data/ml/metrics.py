import cdf
import numpy as np

def F_measure(Y_true, Y_pred):
    P = N = TP = TN = 0
    for i in range(0,len(Y_true)):
        if (Y_true[i] == 1 and Y_pred[i] == 1):
            P += 1
            TP += 1
        if (Y_true[i] == 1 and Y_pred[i] == -1):
            P += 1
        if (Y_true[i] == -1 and Y_pred[i] == 1):
            N += 1
        if (Y_true[i] == -1 and Y_pred[i] == -1):
            N += 1
            TN += 1            
    return (TP/float(P) + 2*TN/float(N))/3.0

def S_measure(all_scores, default_scores):
    cf = cdf.CumulativeFunction(all_scores)
    s = 0
    num_ds = len(default_scores)
    for i in range(0, num_ds):
        s += cf(default_scores[i])
    return 1-1/float(num_ds) * s


