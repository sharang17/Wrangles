from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
import numpy as np
import pandas as pd

########################################################
def det_best(label_test,features):
    #result=[]
    best_acc=-1.0
    cols=features.shape[1]
    for i in range(cols):
        thresh=features[:,i]
        for t in thresh:
            f_i=features[:,i]
            pred=(f_i>t)
            acc=(pred==label_test).mean()
            rev_acc=(pred==~label_test).mean()
            if rev_acc>acc:
                reverse=True
                acc=rev_acc
            else:
                reverse=False
            if acc>best_acc:
                best_acc=acc
                best_i=i
                best_t=t
                best_reverse=reverse
    results=best_t,best_i,best_reverse
    return results
##########################################################################
def plot_classifier(name,label_test,results,features,feature_names,COLOR_FIGURE):
    if COLOR_FIGURE:
        area1c=(1.,.8,.8)
        area2c=(.8,.8, 1.)
    else:
        area1c=(1.,1.,1.)
        area2c=(.7,.7,.7)
    t=results[0]
    f0=results[1]
    if name=="virginica" or name=="setosa":
        f1=f0-1
    else:
        f1=f0+1
    label1=name
    label2="Not "+name
    fig,ax=plt.subplots()
    x0=features[:,f0].min()*.9
    x1=features[:,f0].max()*1.1
    y0=features[:,f1].min()*.9
    y1=features[:,f1].max()*1.1
    ax.fill_between([x0,t],[y0,y0],[y1,y1],color=area2c)
    ax.fill_between([t,x1],[y0,y0],[y1,y1],color=area1c)
    ax.plot([t,t],[y0,y1],"k--",lw=2)
    ax.scatter(features[label_test,f0],features[label_test,f1],c="b",marker="o",s=40,label=label1)
    ax.scatter(features[~label_test,f0],features[~label_test,f1],c="r",marker="x",s=40,label=label2)
    ax.set_ylim(y0,y1)
    ax.set_xlim(x0,x1)
    ax.set_xlabel(feature_names[f0])
    ax.set_ylabel(feature_names[f1])
    ax.legend()
    plt.show()

#####################################################################################################
def predict(model,features):
    t,fi,reverse=model
    if reverse:
        return features[:, fi] <= t
    else:
        return features[:,fi]>t

#####################################################################################################
COLOR_FIGURE=False
data=load_iris()
features=data["data"]
feature_names=data["feature_names"]
target=data["target"]
print target

target_names=data["target_names"]
labels=target_names[target]
is_setosa=labels=="setosa"
is_virginica=labels=="virginica"
is_versicolor=labels=="versicolor"
tests=[is_setosa,is_virginica,is_versicolor]
names=["virginica","setosa","versicolor"]
#for i in range(3):
#    results=det_best(tests[i],features)
#    plot_classifier(names[i],tests[i],results,features,feature_names,COLOR_FIGURE)

########################################################################################################

correct=0
for ei in range(len(features)):
    training=np.ones(len(features),bool)
    training[ei]=False
    testing=~training
    model=det_best(is_versicolor[training],features[training])
    predictions=predict(model,features[testing])
    correct += np.sum(predictions == is_virginica[testing])
acc = correct/float(len(features))
print('Accuracy: {0:.1%}'.format(acc))
