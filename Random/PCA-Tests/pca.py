import numpy as np
import matplotlib.pyplot as plt
data=open('C:\Users\Sharang Bhat\Documents\GitHub\Wrangles\Random\PCA-Tests\USAIR.DAT','r').readlines()
data=[i.strip().split('\t') for i in data]
data=np.array([[float(j) for j in i] for i in data])
m,n=data.shape


####Step-1-Mean center the data
mdata=data-np.mean(data,axis=0)
#print mdata

####Step2- Find covariance matrix-Take transpose of the original matrix

cvr_mdata=np.cov(mdata.T)
s = '{:10.2f} '*n
#for i in range(n):
#    print s.format(*cvr_mdata[i])

eigenvalues,eigenvector=np.linalg.eig(cvr_mdata)

srt_eigenvalues=np.argsort(eigenvalues)[::-1]
eigenvector=np.matrix(eigenvector[:,srt_eigenvalues])
eigenvalues=eigenvalues[srt_eigenvalues]
#print s.format(*eigenvalues)
"""
plt.semilogy(eigenvalues.real,'-o')
plt.title("Log-plot of Eigenvalues")
plt.xlabel( "Eigenvalue Index" )
plt.ylabel( "Eigenvalue Magnitude" )
plt.grid() ; plt.savefig( "eigenvalue_logplot.png", fmt="png", dpi=200 )
"""

n_pc=3
fv=eigenvector[:,:n_pc]
pca=fv.T*mdata.T
print pca
