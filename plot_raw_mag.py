#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 12:22:13 2020

@author: mtc-20
"""
import pandas as pd
import numpy as np
data = pd.read_csv('plot_zulu.csv')
df = pd.DataFrame(np.array(data) , columns=['x','y','z'])
df.describe()

df.plot(x='y',y='x',kind='scatter', figsize=(5,5))



data_HO =  pd.read_csv('HO_zulu.csv')
df_HO = pd.DataFrame(np.array(data_HO) , columns=['x','y','z'])
df_HO.plot(x='x',y='y',kind='scatter', figsize=(5,5))

data_SO =  pd.read_csv('SO_zulu.csv')
df_SO = pd.DataFrame(np.array(data_SO) , columns=['x','y','z'])
df_SO.plot(x='x',y='y',kind='scatter', figsize=(5,5))