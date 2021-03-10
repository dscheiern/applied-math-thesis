# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 21:04:43 2020

@author: Delaney

Description:
    -   Uses Census API to get data from ACS about types of health care insurance
        for each county in the United States
    -   Removes invalid data
    -   Transforms data into proportions of county populations in each insurance category
    -   Saves raw and transformed data as CSVs
"""


from census import Census
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

c = Census("CENSUS_API_KEY")

my_codes_gen = ['B01001_001E','B10010_001E']
my_codes_va = ['B27010_009E','B27010_025E','B27010_041E','B27010_057E']
my_codes_emp = ['B27010_004E','B27010_020E','B27010_036E','B27010_053E']
my_codes_medicare = ['B27010_006E','B27010_022E','B27010_038E','B27010_055E']
my_codes_private = ['B27010_005E','B27010_021E','B27010_037E','B27010_054E']
my_codes_none = ['B27010_017E','B27010_033E','B27010_050E','B27010_066E']
my_codes_two = ['B27010_010E','B27010_026E','B27010_042E','B27010_058E']
my_codes_caid = ['B27010_007E','B27010_023E','B27010_039E']
all_codes = my_codes_gen + my_codes_va + my_codes_emp + my_codes_medicare + my_codes_private + my_codes_none + my_codes_two + my_codes_caid

######################## CODE DESCRIPTIONS ##############################
# B01001_001E: Total population
# B10010_001E: Median income

# B27010_009E: Estimate!!Total!!Under 19 years!!With one type of health insurance coverage!!With VA Health Care only
# B27010_025E: Estimate!!Total!!19 to 34 years!!With one type of health insurance coverage!!With VA Health Care only
# B27010_041E: Estimate!!Total!!35 to 64 years!!With one type of health insurance coverage!!With VA Health Care only
# B27010_057E: Estimate!!Total!!65 years and over!!With one type of health insurance coverage!!With VA Health Care only

# B27010_004E: Estimate!!Total!!Under 19 years!!With one type of health insurance coverage!!With employer-based health insurance only
# B27010_020E: Estimate!!Total!!19 to 34 years!!With one type of health insurance coverage!!With employer-based health insurance only
# B27010_036E: Estimate!!Total!!35 to 64 years!!With one type of health insurance coverage!!With employer-based health insurance only
# B27010_053E: Estimate!!Total!!65 years and over!!With one type of health insurance coverage!!With employer-based health insurance only

# B27010_006E: Estimate!!Total!!Under 19 years!!With one type of health insurance coverage!!With Medicare coverage only
# B27010_022E: Estimate!!Total!!19 to 34 years!!With one type of health insurance coverage!!With Medicare coverage only
# B27010_038E: Estimate!!Total!!35 to 64 years!!With one type of health insurance coverage!!With Medicare coverage only
# B27010_055E: Estimate!!Total!!65 years and over!!With one type of health insurance coverage!!With Medicare coverage only

# B27010_005E: Estimate!!Total!!Under 19 years!!With one type of health insurance coverage!!With direct-purchase health insurance only
# B27010_021E: Estimate!!Total!!19 to 34 years!!With one type of health insurance coverage!!With direct-purchase health insurance only
# B27010_037E: Estimate!!Total!!35 to 64 years!!With one type of health insurance coverage!!With direct-purchase health insurance only
# B27010_054E: Estimate!!Total!!65 years and over!!With one type of health insurance coverage!!With direct-purchase health insurance only

# B27010_017E: Estimate!!Total!!Under 19 years!!No health insurance coverage
# B27010_033E: Estimate!!Total!!19 to 34 years!!No health insurance coverage
# B27010_050E: Estimate!!Total!!35 to 64 years!!No health insurance coverage
# B27010_066E: Estimate!!Total!!65 years and over!!No health insurance coverage

# B27010_010E: Estimate!!Total!!Under 19 years!!With two or more types of health insurance coverage
# B27010_026E: Estimate!!Total!!19 to 34 years!!With two or more types of health insurance coverage
# B27010_042E: Estimate!!Total!!35 to 64 years!!With two or more types of health insurance coverage
# B27010_058E: Estimate!!Total!!65 years and over!!With two or more types of health insurance coverage

# B27010_007E: Estimate!!Total!!Under 19 years!!With one type of health insurance coverage!!With Medicaid/means-tested public coverage only
# B27010_023E: Estimate!!Total!!19 to 34 years!!With one type of health insurance coverage!!With Medicaid/means-tested public coverage only
# B27010_039E: Estimate!!Total!!35 to 64 years!!With one type of health insurance coverage!!With Medicaid/means-tested public coverage only



better_names = {'B01001_001E':'Population',
                'B10010_001E':'Median_Income',
                'B27010_009E':'VA_HC_under19',
                'B27010_025E':'VA_HC_19to34',
                'B27010_041E':'VA_HC_35to64',
                'B27010_057E':'VA_HC_65over',
                'B27010_004E':'Emp_HC_under19',
                'B27010_020E':'Emp_HC_19to34',
                'B27010_036E':'Emp_HC_35to64',
                'B27010_053E':'Emp_HC_65over',
                'B27010_006E':'Mcare_HC_under19',
                'B27010_022E':'Mcare_HC_19to34',
                'B27010_038E':'Mcare_HC_35to64',
                'B27010_055E':'Mcare_HC_65over',
                'B27010_005E':'Priv_HC_under19',
                'B27010_021E':'Priv_HC_19to34',
                'B27010_037E':'Priv_HC_35to64',
                'B27010_054E':'Priv_HC_65over',
                'B27010_017E':'None_HC_under19',
                'B27010_033E':'None_HC_19to34',
                'B27010_050E':'None_HC_35to64',
                'B27010_066E':'None_HC_65over',
                'B27010_010E':'Two_HC_under19',
                'B27010_026E':'Two_HC_19to34',
                'B27010_042E':'Two_HC_35to64',
                'B27010_058E':'Two_HC_65over',
                'B27010_007E':'Caid_HC_under19',
                'B27010_023E':'Caid_HC_19to34',
                'B27010_039E':'Caid_HC_35to64'}



data = c.acs5.state_county(all_codes, Census.ALL, Census.ALL)
df1 = pd.DataFrame(data, columns =['state','county']+all_codes)
print(df1)

df1 = df1.rename(columns=better_names)

df1['All_VA'] = df1['VA_HC_under19'] + df1['VA_HC_19to34'] + df1['VA_HC_35to64'] + df1['VA_HC_65over']
df1['Per_VA'] = df1['All_VA']/df1['Population']
df1['All_Emp'] = df1['Emp_HC_under19'] + df1['Emp_HC_19to34'] + df1['Emp_HC_35to64'] + df1['Emp_HC_65over']
df1['Per_Emp'] = df1['All_Emp']/df1['Population']
df1['All_Medicare'] = df1['Mcare_HC_under19'] + df1['Mcare_HC_19to34'] + df1['Mcare_HC_35to64'] + df1['Mcare_HC_65over']
df1['Per_Medicare'] = df1['All_Medicare']/df1['Population']
df1['All_Private'] = df1['Priv_HC_under19'] + df1['Priv_HC_19to34'] + df1['Priv_HC_35to64'] + df1['Priv_HC_65over']
df1['Per_Private'] = df1['All_Private']/df1['Population']
df1['All_None'] = df1['None_HC_under19'] + df1['None_HC_19to34'] + df1['None_HC_35to64'] + df1['None_HC_65over']
df1['Per_None'] = df1['All_None']/df1['Population']
df1['All_Two'] = df1['Two_HC_under19'] + df1['Two_HC_19to34'] + df1['Two_HC_35to64'] + df1['Two_HC_65over']
df1['Per_Two'] = df1['All_Two']/df1['Population']
df1['All_Caid'] = df1['Caid_HC_under19'] + df1['Caid_HC_19to34'] + df1['Caid_HC_35to64']
df1['Per_Caid'] = df1['All_Caid']/df1['Population']

df1['county_FIPS'] = df1['state'] + df1['county']

for_project = df1[['county_FIPS','Population','Median_Income','Per_VA','Per_Emp','Per_Medicare','Per_Private','Per_None','Per_Two','Per_Caid']]

for_project_clean = df1[['county_FIPS','Population','Median_Income','Per_VA','Per_Emp','Per_Medicare','Per_Private','Per_None','Per_Two','Per_Caid']]
for_project_clean = for_project_clean.loc[for_project_clean['Median_Income'] >= 0,:]

for_project.to_csv(r'data\healthcare_stats.csv')
for_project_clean.to_csv(r'data\healthcare_stats_clean.csv')
