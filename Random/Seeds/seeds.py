from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

#def plot_decision(features,labels)

def load():
    data = []
    labels = []
    with open('C:\Users\Sharang Bhat\Documents\GitHub\Wrangles\Random\Seeds\seeds.tsv') as ifile:
        for line in ifile:
            tokens = line.strip().split('\t')
            data.append([float(tk) for tk in tokens[:-1]])
            labels.append(tokens[-1])
    data = np.array(data)
    labels = np.array(labels)
    return data, labels

def plot_decision(features,labels,feature_names,names):
    COLOR_FIGURE=False
    y0,y1=features[:,2].min() *.9,features[:,2].max() *1.1
    x0,x1=features[:,0].min()*.9,features[:,0].max()*1.1
    X=np.linspace(x0,x1,1000)
    Y=np.linspace(y0,y1,1000)
    X,Y=np.meshgrid(X,Y)
    model=KNeighborsClassifier(n_neighbors=1)
    model.fit(features[:,(0,2)],labels)
    C=model.predict(np.vstack([X.ravel(),Y.ravel()]).T).reshape(X.shape)
    if COLOR_FIGURE:
        cmap=ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
    else:
        cmap=ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
    fig,ax=plt.subplots()
    ax.set_xlim(x0,x1)
    ax.set_ylim(y0,y1)
    ax.set_xlabel(feature_names[0])
    ax.set_ylabel(feature_names[2])
    ax.pcolormesh(X,Y,C,cmap=cmap)
    cmap = ListedColormap(['red', 'green', 'blue'])
    ax.scatter(features[:, 0], features[:, 2], marker="x",c=labels, cmap=cmap,label=names)
    fig.tight_layout()
    plt.title("Nearest Neighbour Classification for Seeds Dataset")
    plt.show()



feature_names = [
    'area',
    'perimeter',
    'compactness',
    'length of kernel',
    'width of kernel',
    'asymmetry coefficien',
    'length of kernel groove',
]
features,labels=load()
names=sorted(set(labels))
labels = np.array([names.index(ell) for ell in labels])
#print labels
#plot_decision(features,labels,feature_names,names)
