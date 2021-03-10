# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:10:50 2020

@author: Delaney

Description: 
    -   Performs both k-Means and Gaussian Mixture Model clustering with
        2-50 clusters of health insurance census data
    -   Compares Davies-Bouldin Index and Silhouette Index for k-Means and GMM
        by plotting
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics

data = pd.read_csv((r'\data\hc_environ_stats.csv'),index_col=0)
data = data.drop(["county_FIPS","Median_Income","Population","pm","benz","form","ace"], axis=1)
data = data.reset_index(drop=True, level=0)

###########################################################################
### K-MEANS
from sklearn.cluster import KMeans

k_data = data.copy()
dbi = []
sil = []
inertia = []
flat = pd.DataFrame()
for i in range(2,50):
    kmeans = KMeans(n_clusters = i)
    kmeans.fit(k_data)

    pred = kmeans.labels_
    inertia.append(kmeans.inertia_)
    dbi.append(metrics.davies_bouldin_score(k_data, pred))
    sil.append(metrics.silhouette_score(k_data, pred, metric='euclidean'))

k_res = pd.DataFrame(columns = ['dbi','sil'])
k_res['dbi'] = dbi
k_res['sil'] = sil
k_res['iner'] = inertia

##############################################################################
### GAUSSIAN MIXTURE MODEL
from sklearn.mixture import GaussianMixture

gmm_data = data.copy()
print('gmm:')
print(gmm_data)
dbi = []
sil = []
for i in range(2,50):
    gmm = GaussianMixture(n_components = i)
    gmm.fit(gmm_data)

    pred2 = gmm.predict(gmm_data)

    dbi.append(metrics.davies_bouldin_score(gmm_data, pred2))
    sil.append(metrics.silhouette_score(gmm_data, pred2, metric='euclidean'))

gmm_res = pd.DataFrame(columns = ['dbi','sil'])
gmm_res['dbi'] = dbi
gmm_res['sil'] = sil

plt.figure(1)
plt.plot(range(2,50),k_res['dbi'], 'b--',gmm_res['dbi'], 'r--')
plt.suptitle('Davies-Bouldin Index vs. Number of Clusters', fontsize=14)
plt.title('K-Means and Gaussian Mixture Model', fontsize=10, color='green')
plt.xlabel('Number of Clusters')
plt.ylabel('Davies-Bouldin Index')
plt.legend(['K-Means','Gaussian Mixture Model'])

plt.figure(2)
plt.plot(range(2,50),k_res['sil'], 'b--', gmm_res['sil'], 'r--')
plt.suptitle('Silhouette Index vs. Number of Clusters', fontsize=14)
plt.title('K-Means and Gaussian Mixture Model', fontsize=10, color='green')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Index')
plt.legend(['K-Means','Gaussian Mixture Model'])

plt.figure(3)
plt.plot(range(2,50),k_res['iner'], 'b--')
plt.suptitle('Sum of Squared Errors vs. Number of Clusters', fontsize=14)
plt.title('K-Means', fontsize=10, color='green')
plt.xlabel('Number of Clusters')
plt.ylabel('Sum of Squared Errors')
