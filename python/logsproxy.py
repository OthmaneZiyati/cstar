# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 11:03:14 2016

@author: lmellior
"""

import pandas as pd
from os import listdir
pd.set_option("display.max_columns",100)
from sklearn.preprocessing import scale
import numpy as np
#from scipy.spatial import distance   
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from collections import Counter
from sklearn import decomposition
import matplotlib.pyplot as plt 


# ------------------------------ Parameters --------------------------------- #

DIR_DATA = "D:/Users/lmellior/Desktop/Sogeti/ESEC/code/output log 50go/"
DBSCAN_EPS = 9
DBSCAN_MINPTS = 15
KMEANS_N_CLUSTERS = 7
NB_JUMPERS = 6


# ------------------------------ Functions --------------------------------- #

def initialization(df):
    # Create new features
    df['Average_duration'] = df['Total_duration'] / df['Nb_logs']
    df['Average_request'] = df['Total_request'] / df['Nb_logs']
    df['Average_responsesize'] = df['Total_responsesize'] / df['Nb_logs'] # diviser par log-POST ?
    
    # Delete UNKNOW username
    df = df[df.username != 'UNKNOWN']
    
    # change index to username 
    df.set_index(['username'], inplace=True)
    df.index.name = None

    # Delete useless columns
    df = df.loc[:,df.sum(axis=0) != 0]
    
    return df

def normalization(df,scaling):
    features_percent=['Nb_weekend','Nb_outsideofficehours','Nb_badport','Nb_cat_adv',
                         'Nb_cat_gamb','Nb_cat_hack','Nb_cat_ilac','Nb_cat_susp','Nb_cat_p2p','Nb_cat_mail',
                         'nb_cat_park','Nb_cat_infr','Nb_POST','Nb_mime_APPL','Nb_mine_APPL_stream','Nb_URL_tunnel',
                         'Nb_Code200','Nb_Code401','Nb_Code403','Nb_Code404','Nb_Code407','Nb_Code500','Nb_Code501',
                         'Nb_error_code','Total_duration','Total_request',
                         'Total_responsesize','Nb_block_admin','Nb_ip_in_url','Nb_TCP_denied','Nb_TCP_miss']
 
    for col in features_percent:
        if col in df.columns:
            df[col] = df[col] / df["Nb_logs"]
    
    if scaling:
        df.loc[:, df.columns != 'username'] = scale(df.loc[:, df.columns != 'username'])
        
    return df


def biplot(data,pc1,pc2):

    pca = decomposition.PCA() 
    pca.fit(data)
    
    axe1 = pc1-1
    axe2 = pc2-1  
    xvector = pca.components_[axe1] # see 'prcomp(my_data)$rotation' in R
    yvector = pca.components_[axe2]
    xs = pca.transform(data)[:,axe1] # see 'prcomp(my_data)$x' in R
    ys = pca.transform(data)[:,axe2]
    
    plt.figure(figsize=(10,6))
    for i in range(len(xvector)):
        plt.arrow(0, 0, xvector[i]*max(xs), yvector[i]*max(ys),
                  color='r', width=0.0005, head_width=0.0025)
        plt.text(xvector[i]*max(xs)*1.2, yvector[i]*max(ys)*1.2,
                 list(data.columns.values)[i], color='g', ha='center', va='center')
    
    for i in range(len(xs)):
        plt.plot(xs[i], ys[i],'bo',alpha=0.2)
        
    plt.show()
    
    
def distance(x,y):   
    return np.sqrt((np.sum(x-y,axis=1))**2)
    
    
# ------------------------------ Read data --------------------------------- #
    
data_files = [file for file in listdir(DIR_DATA) if file.endswith(".csv")]
features = ['username','Nb_logs','Nb_weekend','Nb_outsideofficehours','Nb_badport','Nb_cat_adv',
            'Nb_cat_gamb','Nb_cat_hack','Nb_cat_ilac','Nb_cat_susp','Nb_cat_p2p','Nb_cat_mail',
            'nb_cat_park','Nb_cat_infr','Nb_POST','Nb_mime_APPL','Nb_mine_APPL_stream','Nb_URL_tunnel',
            'Nb_Code200','Nb_Code401','Nb_Code403','Nb_Code404','Nb_Code407','Nb_Code500','Nb_Code501',
            'Max_duration','Max_request','Max_responsesize','Nb_error_code','Total_duration','Total_request',
            'Total_responsesize','Nb_block_admin','Nb_ip_in_url','Nb_TCP_denied','Nb_TCP_miss']

### Data day 1
df_1 = pd.read_csv(DIR_DATA+'2015-12-02_userbase.csv', header=None, names = features) # (11882, 36)
df_1 = initialization(df_1) # (11881, 35)
df_1 = normalization(df_1,scaling=True)

### Data day 2
df_2 = pd.read_csv(DIR_DATA+'2015-12-03_userbase.csv', header=None, names = features) # (11882, 36)
df_2 = initialization(df_2) # (11881, 35)
df_2 = normalization(df_2,scaling=True)


# ------------------------------ DBSCAN  --------------------------------- #

db_scan = DBSCAN(eps=DBSCAN_EPS, min_samples=DBSCAN_MINPTS).fit(df_1)
cluster = [i for i in list(set(db_scan.labels_)) if i != -1]
print('Estimated number of clusters: %d' % len(cluster))
for k in cluster:
    print('clusters %d' % k,'--> %d users'% len([1 for i in db_scan.labels_ if i == k]))
print('* noise * ---> %d users'% len([1 for i in db_scan.labels_ if i == -1]))

# Delete dbscan anomalies
df_ano = df_1.loc[db_scan.labels_ == -1,:]
df_1_clean = df_1.loc[db_scan.labels_ != -1,:]


# ------------------------------ K-means --------------------------------- #

kmeans = KMeans(init='k-means++', n_clusters=KMEANS_N_CLUSTERS, n_init=30, 
                max_iter=100, random_state = 10)
kmeans.fit(df_1_clean)
print(Counter(kmeans.labels_))
center_cluster = pd.DataFrame(kmeans.cluster_centers_, columns = df_1_clean.columns)
center_cluster.index = ['C1','C2','C3','C4','C5','C6','C7']

#df_clean['cluster']=kmeans.labels_
#center_cluster['cluster']=range(0,7)
# -> Bigdata.loc[:, Bigdata.columns != 'cluster']
Bigdata = pd.concat([df_1_clean,center_cluster], axis=0)


# ------------------------------ PCA --------------------------------- #

pca = decomposition.PCA()
pca.fit(Bigdata)
X = pca.transform(Bigdata)
#plt.scatter(X[:,0], X[:,1])
#plt.scatter(X[:,0], X[:,1],c=Bigdata.cluster)
#plt.show()


comp = pd.DataFrame(pca.components_.T, index=Bigdata.columns)

comp_cluster = pd.DataFrame(X[-KMEANS_N_CLUSTERS:], index=center_cluster.index)


#print(pca.explained_variance_ratio_)
#biplot(Bigdata.loc[:, Bigdata.columns != 'cluster'],1,2)


# ------------------------------ Jumpers --------------------------------- #

shared_users = list(set(df_1_clean.index) & set(df_2.index))
dist = pd.DataFrame(shared_users, columns = ['username']) 
dist['d'] = distance(df_1_clean.loc[shared_users,:].values,
                        df_2.loc[shared_users,:].values)

# sort by distance max
dist.sort_values(['d'], ascending=False,inplace=True)
jumpers = dist.username[0:NB_JUMPERS]
jump1 = df_1.loc[jumpers,:]
jump2 = df_2.loc[jumpers,:]


# 
xstart = np.dot(pca.components_[0],jump1.T)
xend = np.dot(pca.components_[0],jump2.T)

ystart = np.dot(pca.components_[1],jump1.T)
yend = np.dot(pca.components_[1],jump2.T)















