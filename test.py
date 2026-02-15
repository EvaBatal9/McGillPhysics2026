import numpy as np

array1 = [1, 2, 3, 4, 5]

array2 = [6, 7, 8, 9, 10]

array_total = np.array([array1, array2])
sum_column1 = np.sum(array_total, axis=0)
print(sum_column1)

print(array1)