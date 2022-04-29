import numpy as np
from collections import Counter

# Create your matrix
a = np.array([[ 1,  0, -1],
              [ 1,  1,  0],
              [-1,  0,  1],
              [ 0,  1,  0]])

# Loop on each column to get the most frequent element and its count
a[0][1] = 12
print(a)
count = Counter(a[:, 0])
print(count)
# for i in range(a.shape[1]):
#     count = Counter(a[:, 2])
#     print(count)
#     count.most_common(1)