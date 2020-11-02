import pandas as pd
import numpy as np

X = ['a (per 1000)__weighted_ratio', 'a (per 1000)__weight', 'a']

x = 'a c__weighted_ratio'

ratio_markers = ['coverage', 'per 10']

# filter_col = [x for x in X if (
#     (x.endswith('__weighted_ratio') or (x.endswith('__weight'))))]

Z = X + [x]

print(Z)
