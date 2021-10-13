import scipy.io as io

df = io.loadmat("private/tsdata2f.mat", squeeze_me=True)
df = io.matlab.mio5.varmats_from_mat(open("private/tsdata2f.mat", "rb"))
print(df)

# import numpy as np
# import h5py
# f = h5py.File('private/2020-08-10.mat','r')
# data = f.get('data/variable1')
# data = np.array(data) # For converting to a NumPy array

# import tables
# file = tables.open_file('private/2020-08-10.mat')
