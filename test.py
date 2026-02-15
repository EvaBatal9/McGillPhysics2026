import numpy as np
import scipy.fft as sp

array1 = [1, 2, 3, 4, 5]

array2 = [6, 7, 8, 9, 10]

array_total = np.array([array1, array2])
sum_column1 = np.sum(array_total, axis=0)
print(sum_column1)

array3 = sp.fft(array1)
