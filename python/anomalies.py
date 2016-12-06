# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:26:34 2016

@author: lmellior

This script compute the distance to the barycentre and the contribution 
of each features to this center.

-> load data
-> initialization & normalization of data
-> dbscan
-> kmeans (except dbscan anomalies )
-> f(barycentreDistance)
-> cluster name and sort by distance max
"""
# ------------------------------ Libraries --------------------------------- #

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
#NB_JUMPERS = 6

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


def barycentreDistance(df) :
    barycentre = [np.mean(df[feature]) for feature in df.columns]
    temp = (df - barycentre)**2
    tot = np.sum(temp,axis=1)
    d = 100*temp.div(tot, axis=0)
    d['dist']=np.sqrt(tot)
    return d.round(4) 
# ------------------------------ Read data --------------------------------- #
    
data_files = [file for file in listdir(DIR_DATA) if file.endswith(".csv")]
features = ['username','Nb_logs','Nb_weekend','Nb_outsideofficehours','Nb_badport','Nb_cat_adv',
            'Nb_cat_gamb','Nb_cat_hack','Nb_cat_ilac','Nb_cat_susp','Nb_cat_p2p','Nb_cat_mail',
            'nb_cat_park','Nb_cat_infr','Nb_POST','Nb_mime_APPL','Nb_mine_APPL_stream','Nb_URL_tunnel',
            'Nb_Code200','Nb_Code401','Nb_Code403','Nb_Code404','Nb_Code407','Nb_Code500','Nb_Code501',
            'Max_duration','Max_request','Max_responsesize','Nb_error_code','Total_duration','Total_request',
            'Total_responsesize','Nb_block_admin','Nb_ip_in_url','Nb_TCP_denied','Nb_TCP_miss']

### Data day 1
df = pd.read_csv(DIR_DATA+'2015-12-02_userbase.csv', header=None, names = features) # (11882, 36)
df = initialization(df) # (11881, 35)
df = normalization(df,scaling=True)

# DBSCAN
db_scan = DBSCAN(eps=DBSCAN_EPS, min_samples=DBSCAN_MINPTS).fit(df)
df_clean = df.loc[db_scan.labels_ != -1,:]
#df_ano = df.loc[db_scan.labels_ == -1,:]

# KMEANS
kmeans = KMeans(init='k-means++', n_clusters=KMEANS_N_CLUSTERS, n_init=30, 
                max_iter=100, random_state = 10).fit(df_clean)
df_clean['cluster']=kmeans.labels_

# Distance to barycentre 
df = barycentreDistance(df)

# Add kmeans cluster to the dataframe
df['cluster'] = 99
for username in df_clean.index:
    df.loc[username,'cluster'] = df_clean.loc[username,'cluster']

# Add cluster names
df.loc[df.cluster == 0,'cluster'] = 'C1'
df.loc[df.cluster == 1,'cluster'] = 'C2'
df.loc[df.cluster == 2,'cluster'] = 'C3'
df.loc[df.cluster == 3,'cluster'] = 'C4'
df.loc[df.cluster == 4,'cluster'] = 'C5'
df.loc[df.cluster == 5,'cluster'] = 'C6'
df.loc[df.cluster == 6,'cluster'] = 'C7'
df.loc[df.cluster == 99,'cluster'] = 'dbscan'

# Sort by distance max
df.sort_values(['dist'], ascending=False,inplace=True)




    

