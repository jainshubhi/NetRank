# CS 145 Netrank
# Shubhi Jain & Ricky Galliani
# Code from https://stanford.edu/~mwaskom/software/seaborn/examples/many_pairwise_correlations.html

from string import letters
from itertools import combinations
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="white")

# Generate a large random dataset
tr_rpi = pd.read_csv('../data/basketball/team_ranking/2010_2011/2011_04_04.csv')
ours = pd.read_csv('../results/basketball/np/2010_2011/04_04_2011.csv')

# Generate correlation matrix
all_pairs = combinations(tr_rpi['team'].tolist(), 2)

for 

rs = np.random.RandomState(33)
d = pd.DataFrame(data=rs.normal(size=(100, 26)),
                 columns=list(letters[:26]))

print d

# Compute the correlation matrix
corr = d.corr()

print corr

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3,
            square=True, xticklabels=5, yticklabels=5,
            linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
