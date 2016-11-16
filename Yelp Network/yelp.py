import pandas as pd
import numpy as np
import json
from scipy import sparse
business=pd.read_csv('yelp_business.csv')
reviews=pd.read_csv('yelp_reviews.csv')
users=pd.read_csv('yelp_users.csv')

user_unique=reviews['user_id'].unique()
business_unique=reviews['business_id'].unique()

user_dict={}
business_dict={}
for i in range(0,len(user_unique)):
    temp={user_unique[i]:i}
    user_dict.update(temp)

biz_1={reviews['business_id'][0]:len(reviews['business_id'])+1}
business_dict.update(biz_1)
for i in range(1,len(business_unique)):
    temp={business_unique[i]:business_dict.get(business_unique[i-1])+1}
    business_dict.update(temp)

user_no=[]
business_no=[]
for i in range(0,len(reviews['review_id'])):
    user_no.append(user_dict.get(reviews['user_id'][i]))
    business_no.append(business_dict.get(reviews['business_id'][i]))

n=len(user_no)+len(business_no)
def dataset2dok():
        dokm = sparse.dok_matrix((n,n),dtype=np.bool)
        for i in range(0,len(user_no)):
            origin, destiny = user_no[i],business_no[i]
            dokm[destiny,origin]=True
        return(dokm.tocsr())

def compute_PageRank(G, beta=0.85, epsilon=10**-4):
    '''
    Efficient computation of the PageRank values using a sparse adjacency 
    matrix and the iterative power method.
    
    Parameters
    ----------
    G : boolean adjacency matrix. np.bool8
        If the element j,i is True, means that there is a link from i to j.
    beta: 1-teleportation probability.
    epsilon: stop condition. Minimum allowed amount of change in the PageRanks
        between iterations.

    Returns
    -------
    output : tuple
        PageRank array normalized top one.
        Number of iterations.

    '''    
    #Test adjacency matrix is OK
    n,_ = G.shape
    assert(G.shape==(n,n))
    #Constants Speed-UP
    deg_out_beta = G.sum(axis=0).T/beta #vector
    #Initialize
    ranks = np.ones((n,1))/n #vector
    time = 0
    flag = True
    while flag:        
        time +=1
        with np.errstate(divide='ignore'): # Ignore division by 0 on ranks/deg_out_beta
            new_ranks = G.dot((ranks/deg_out_beta)) #vector
        #Leaked PageRank
        new_ranks += (1-new_ranks.sum())/n
        #Stop condition
        if np.linalg.norm(ranks-new_ranks,ord=1)<=epsilon:
            flag = False        
        ranks = new_ranks
    return(ranks, time)


csr=dataset2dok()
pr,iters=compute_PageRank(csr)
reviews['user_no']=pd.Series(user_no)
reviews['business_no']=pd.Series(business_no)

