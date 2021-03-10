# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 09:20:29 2020

@author: Delaney

Description:
    -   Creates/runs Genetic Algorithm as described in 'final_paper.pdf'
    -   Initializes chromosomes with density protocol
    -   Assigns clusters based on Euclidean distance
    -   Fitness function based on sum of squared errors with penalty for large cluster size
    -   Crossover and mutation with adaptive probability protocols
    -   Saves progress of clusters throughout
    -   Runs genetic algorithm with 70 chromosomes for 75 generations on health insurance census data
"""

import pandas as pd
from sklearn import metrics
import numpy as np
import random


def setup(pop_size, r):
    X = pd.read_csv((r'data\hc_environ_stats.csv'),index_col=0)
    X = X.drop(["county_FIPS","Median_Income","Population","pm","benz","form","ace"], axis=1)
    X = X.reset_index(drop=True, level=0)

    [n,m] = X.shape
    V = X.apply(lambda v: (v-v.min())/(v.max()-v.min()), axis=0)
    return [X, V, n, m, r]

def init_chroms(pop_size, r, V):
    pairs = metrics.pairwise_distances(V)
    pairs = pd.DataFrame(pairs)
    all_chroms = pd.DataFrame()
    for x in range(pop_size):
        r_x = r[x]
        dens = pairs[pairs <= r_x].count()
        max_value = dens.max()
        chrom = pairs.loc[(dens <= max_value) & (dens > max_value-1),:]
        gap = 2
        while chrom.shape[0] < 5: # guaranteeing this many points in each cluster
            chrom = pairs.loc[(dens <= max_value) & (dens > max_value-gap),:]
            gap = gap + 1
        these_chroms = V.loc[V.index & chrom.index]
        these_chroms = these_chroms.assign(Chrom_ID=x)
        these_chroms = these_chroms.assign(Center_ID=range(chrom.shape[0]))
        all_chroms = pd.concat([all_chroms,these_chroms])
    all_chroms = all_chroms.reset_index(drop=True, level=0)
    return all_chroms

def assignments(pop_size, V, chrom_df):
    all_assignments = pd.DataFrame()
    for ch in range(pop_size):
        row_assign = np.full(V.shape[0], np.nan)
        sub = chrom_df.loc[chrom_df['Chrom_ID'] == ch]
        dist = pd.DataFrame(metrics.pairwise_distances(V, sub.iloc[:,0:-2]))
        for center in range(dist.shape[1]):
            smalls = np.array(dist.nsmallest(3, center, keep='all').index.tolist())
            row_assign[smalls] = center
        for obs in range(len(row_assign)):
            if not np.isnan(row_assign[obs]):
                continue
            closest_center = dist.iloc[obs,:].nsmallest(1).index[0]
            row_assign[obs] = closest_center
        all_assignments = all_assignments.append(pd.Series(row_assign), ignore_index=True)
    return all_assignments

def fitness(pop_size, chrom_df, all_assignments, V):
    fits = np.full(pop_size, np.nan)
    for ch in range(pop_size):
        sub = chrom_df.loc[chrom_df['Chrom_ID'] == ch]
        temp_sum = 0
        for center in range(sub.shape[0]):
            this_cen = sub.loc[sub['Center_ID'] == center].iloc[:,0:-2]
            indices = V.index[(all_assignments.iloc[:,:] == center).loc[ch,:] == True].tolist()
            inClust = V.iloc[list(indices),:]
            diff = inClust.subtract(np.tile(this_cen,(inClust.shape[0],1)), axis=1)
            temp_fit = np.einsum('ij,ij->i', diff, diff)
            temp_sum += temp_fit.sum()
        temp_sum += (sub.shape[0]/2)**2 # penalty for too many clusters
        fits[ch] = 1/temp_sum
    return fits

def selection(fits, pop_size, chrom_df, V):
    pop_c = crossover(fits, pop_size, chrom_df)
    pop_c = pop_c.reset_index(drop=True, level=0)
    assigns = assignments(pop_size, V, pop_c)
    fits = fitness(pop_size, pop_c, assigns, V)
    pop_m = mutation(fits, pop_size, pop_c)
    return pop_m

def crossover(fits, pop_size, chrom_df):
    rwprobs = [fits[x]/fits.sum() for x in range(len(fits))]
    pop_cross = pd.DataFrame()
    curr_id = 0
    for ch in range(int(pop_size/2)):
        [cr1, cr2] = random.choices(range(pop_size), weights = rwprobs, k = 2)
        fprime = max([fits[cr1],fits[cr2]])
        p_cross = (fits.max() - fprime)/(fits.max()-fits.mean())
        prob_check = random.random()
        centers1 = chrom_df.loc[chrom_df['Chrom_ID'] == cr1]
        centers2 = chrom_df.loc[chrom_df['Chrom_ID'] == cr2]
        if prob_check <= p_cross:
            if centers1.shape[0] == 2 & centers2.shape[0] == 2:
                mid1 = 1
                mid2 = 1
            elif centers1.shape[0] == 2:
                mid1 = 1
                mid2 = random.randint(1,centers2.shape[0]-2)
            elif centers2.shape[0] == 2:
                mid2 = 1
                mid1 = random.randint(1,centers1.shape[0]-2)
            else:
                mid1 = random.randint(1,centers1.shape[0]-2)
                mid2 = random.randint(1,centers2.shape[0]-2)

            off1start = centers1.loc[(centers1['Center_ID'] >= 0) | (centers1['Center_ID'] < mid1),:]
            off1end = centers2.loc[centers2['Center_ID'] >= mid2,:]
            off1 = off1start.append(off1end)
            off1 = off1.assign(Chrom_ID=curr_id)
            off1 = off1.assign(Center_ID=range(off1.shape[0]))
            curr_id += 1

            off2start = centers2.loc[(centers2['Center_ID'] >= 0) | (centers2['Center_ID'] < mid2),:]
            off2end = centers1.loc[centers1['Center_ID'] >= mid1,:]
            off2 = off2start.append(off2end)
            off2 = off2.assign(Chrom_ID=curr_id)
            off2 = off2.assign(Center_ID=range(off2.shape[0]))
            curr_id += 1

            pop_cross = pop_cross.append(off1)
            pop_cross = pop_cross.append(off2)
        else:
            centers1 = centers1.assign(Chrom_ID=curr_id)
            centers1 = centers1.assign(Center_ID=range(centers1.shape[0]))
            curr_id += 1
            centers2 = centers2.assign(Chrom_ID=curr_id)
            centers2 = centers2.assign(Center_ID=range(centers2.shape[0]))
            curr_id += 1
            pop_cross = pop_cross.append(centers1)
            pop_cross = pop_cross.append(centers2)
    return pop_cross.sort_values(['Chrom_ID','Center_ID'])

def mutation(fits, pop_size, chrom_df):
    p_mut = np.array([0.5*(fits.max()-fits[x])/(fits.max()-fits.mean()) for x in range(len(fits))])
    p_mut[p_mut > 1] = 0.5
    pop_mut = pd.DataFrame()
    for ch in range(pop_size):
        centers = chrom_df.loc[chrom_df['Chrom_ID'] == ch,:]
        ran = random.random()
        if ran <= p_mut[ch]:
            i = random.randint(0,centers.shape[0]-1)
            [mx, mn] = [centers.loc[centers['Center_ID'] == i].iloc[:,0:-2].max(axis=1), centers.loc[centers['Center_ID'] == i].iloc[:,0:-2].min(axis=1)]
            temp_row = centers.loc[centers['Center_ID'] == i,:]
            temp_vals = temp_row.iloc[:,0:-2]
            row = temp_vals.copy()
            row += ran*(mx.iat[0]-mn.iat[0])
            row = row.assign(Chrom_ID=ch)
            row = row.assign(Center_ID=i)
            ind = centers.index[centers['Center_ID'] == i].tolist()
            centers = centers.copy().drop(index=ind) # needed to reindex before mutation
            centers = centers.append(row)
            centers = centers.sort_values('Center_ID')
            pop_mut = pop_mut.append(centers)
        else:
            pop_mut = pop_mut.append(centers)
    return pop_mut


def main():
    pop_size = 70
    r = list(np.linspace(start=0.04, stop=0.15, num=pop_size))
    [X, V, n, m, r] = setup(pop_size, r)
    all_chroms = init_chroms(pop_size, r, V)
    print('Initialized chromosomes')
    print(all_chroms)
    G = 75 # number generations
    for g in range(G):
        assigns = assignments(pop_size, V, all_chroms)
        print('Assignments for generation {} complete'.format(g))
        assigns.to_csv(r'data\assignsgen{}.csv'.format(g))
        fits = fitness(pop_size, all_chroms, assigns, V)
        print('Fitness for generation {} complete'.format(g))
        pd.Series(fits).to_csv(r'data\fitsgen{}.csv'.format(g))
        pop_m = selection(fits, pop_size, all_chroms, V)
        print('Selection for generation {} complete'.format(g))
        all_chroms = pop_m.reset_index(drop=True, level=0)
        all_chroms.to_csv(r'data\chromsgen{}.csv'.format(g))
        print('GENERATION {} COMPLETE:'.format(g))
        print(all_chroms)
    final_assigns = assignments(pop_size, V, all_chroms)
    final_fits = fitness(pop_size, all_chroms, final_assigns, V)
    pd.Series(final_fits).to_csv(r'data\fits_finalgen.csv')
    final_assigns.to_csv(r'data\assigns_finalgen.csv')


if __name__ == "__main__":
    main()
