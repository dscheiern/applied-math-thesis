# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 09:30:55 2020

@author: Delaney

Description:
    -   Data previously collected from CDC
    -   Reads CSVs and merges all data on county
"""


import pandas as pd
import glob
import os
from functools import reduce

### not used in final ###
df_haa5 = pd.read_csv(r'data\us_haa5_2018.csv')
df_haa5_new = df_haa5.groupby('countyFIPS').agg(
    max_val = pd.NamedAgg(column='Value', aggfunc=max))
print(df_haa5_new)

### not used in final ###
df_ars = pd.read_csv(r'data\us_arsenic_2018.csv')
df_ars_new = df_ars.groupby('countyFIPS').agg(
    max_val = pd.NamedAgg(column='Value', aggfunc=max))
print(df_ars_new)


df_oz = pd.read_csv(r'data\us_ozone_2016.csv')
df_oz_new = df_oz.groupby('countyFIPS').agg(
    max_val = pd.NamedAgg(column='Value', aggfunc=max))
print(df_oz_new)


df_pm = pd.read_csv(r'data\us_pm25_2016.csv')
df_pm_new = df_pm.groupby('countyFIPS').agg(
    max_val = pd.NamedAgg(column='Value', aggfunc=max))
print(df_pm_new)

### not used in final ###
df_rad = pd.read_csv(r'data\us_radium_2018.csv')
df_rad_new = df_rad.groupby('countyFIPS').agg(
    max_val = pd.NamedAgg(column='Value', aggfunc=max))
print(df_rad_new)

### not used in final ###
df_tox = pd.read_csv(r'data\us_toxicInc_2011.csv')
df_tox_new = df_tox.groupby('countyFIPS').agg(
    max_val = pd.NamedAgg(column='Value', aggfunc=max))
print(df_tox_new)

### not used in final ###
df_tthm = pd.read_csv(r'data\us_tthm_2018.csv')
df_tthm_new = df_tthm.groupby('countyFIPS').agg(
    max_val = pd.NamedAgg(column='Value', aggfunc=max))
print(df_tthm_new)


df_airtox = pd.read_csv(r'data\us_airToxins_2011.csv')
df_benz_new = df_airtox[df_airtox['Pollutant'] == 'Pollutant: Benzene'].groupby('countyFIPS').agg(
    max_val = pd.NamedAgg(column='Value', aggfunc=max))
print(df_benz_new)

df_form_new = df_airtox[df_airtox['Pollutant'] == 'Pollutant: Formaldehyde'].groupby('countyFIPS').agg(
    max_val = pd.NamedAgg(column='Value', aggfunc=max))
print(df_form_new)

df_ace_new = df_airtox[df_airtox['Pollutant'] == 'Pollutant: Acetaldehyde'].groupby('countyFIPS').agg(
    max_val = pd.NamedAgg(column='Value', aggfunc=max))
print(df_ace_new)

df_car_new = df_airtox[df_airtox['Pollutant'] == 'Pollutant: Carbon tetrachloride'].groupby('countyFIPS').agg(
    max_val = pd.NamedAgg(column='Value', aggfunc=max))
print(df_car_new)

df_buta_new = df_airtox[df_airtox['Pollutant'] == 'Pollutant: 1,3-butadiene'].groupby('countyFIPS').agg(
    max_val = pd.NamedAgg(column='Value', aggfunc=max))
print(df_buta_new)


all_df = [df_haa5_new, df_ars_new, df_oz_new, df_pm_new, df_rad_new, df_tox_new, df_tthm_new, df_benz_new, df_form_new, df_ace_new, df_car_new, df_buta_new]

df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['countyFIPS'], how='inner'), all_df)
#print(df_merged)

#df_merged.to_csv(r'C:\Users\Delaney\Documents\Colgate\sem\coding\data\all_inner.csv')


#### choosing environmental factors with least amount of missing data ####
full_cou_df = [df_oz_new, df_pm_new, df_benz_new, df_form_new, df_ace_new, df_car_new, df_buta_new]
df_some = reduce(lambda  left,right: pd.merge(left,right,on=['countyFIPS'], how='inner'), full_cou_df)
df_some.columns = ['oz', 'pm', 'benz', 'form', 'ace', 'car', 'buta']
print(df_some)
df_some.to_csv(r'data\bigs_inner.csv')
