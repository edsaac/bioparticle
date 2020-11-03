import numpy as np
import h5py as hdf5

InputFilename = './FLOW/Test.h5'
f = hdf5.File(InputFilename,mode="r")

t_Key  = 'Time:  2.00000E+00 d'
f1 = f[t_Key]

uX_Key = 'Liquid X-Flux Velocities'
uY_Key = 'Liquid Y-Flux Velocities'
uZ_Key = 'Liquid Z-Flux Velocities'
ID_Key = 'Natural_ID'

ID3D = np.transpose(f1[ID_Key],(2,1,0))
NX = np.shape(ID3D)[2]
NY = np.shape(ID3D)[1]
NZ = np.shape(ID3D)[0]

print("(NZ,NY,NX): ",np.shape(ID3D))
print("(NZ,NY,NX): ",NZ,NY,NX)

uX3D = np.transpose(f1[uX_Key],(2,1,0))
uY3D = np.transpose(f1[uY_Key],(2,1,0))
uZ3D = np.transpose(f1[uZ_Key],(2,1,0))

print("uX3D: ",np.shape(uX3D))
print("uY3D: ",np.shape(uY3D))
print("uZ3D: ",np.shape(uZ3D))

fillX = np.zeros((NZ,NY,1))
fillY = np.zeros((NZ,1,NX))
fillZ = np.zeros((1,NY,NX))

uXAdd = np.append(uX3D,fillX,axis=2)
uYAdd = np.append(uY3D,fillY,axis=1)
uZAdd = np.append(uZ3D,fillZ,axis=0)

uX = np.reshape(uXAdd,-1)
uY = np.reshape(uYAdd,-1)
uZ = np.reshape(uZAdd,-1)
ID = np.reshape(ID3D,-1)

daysToSeconds = 1./86400.
uX *= daysToSeconds
uY *= daysToSeconds
uZ *= daysToSeconds

#cellID = np.arange(1,len(uX)+1,dtype="int32")

OutputFilename = './FLOW/ReadyToTransport.h5'
fOUT = hdf5.File(OutputFilename,mode='w')

fOUT.create_dataset('Internal Velocity X', data=uX)
fOUT.create_dataset('Internal Velocity Y', data=uY)
fOUT.create_dataset('Internal Velocity Z', data=uZ)
fOUT.create_dataset('Cell Ids', data=ID)

## Boundary conditions ??
fOUT.create_dataset('leaking_top', data=uZ)
fOUT.create_dataset('noFlowSide_right', data=uX)
fOUT.create_dataset('noFlowSide_left', data=uX)
fOUT.create_dataset('noFlowSide_north', data=uY)
fOUT.create_dataset('noFlowSide_south', data=uY)


fOUT.close()
'''
import sys
import math
from h5py import *
import numpy

filename = 'dataset.h5'
h5file = File(filename,mode='w')

nx = 10
ny = 5
nz = 4
n = nx*ny*nz

# ijk indexed array
ijk_array = numpy.zeros((nx,ny,nz),numpy.float64)

# cell indexed array where each cell id is calculated by i+j*nx+k*nx*ny
# Although indexing here is zero-based, PFLOTRAN will treat it one-based 
# internally.
cell_indexed_array = numpy.zeros((n),numpy.float64)

# FOR ISOTROPIC PERMEABILITY ##################################################
# set values in ijk_array
for k in range(nz):
    for j in range(ny):
        for i in range(nx):
            ijk_array[i][j][k] = 1.e-12+1.e-15*(k+1)+1.e-18*(j+1)+1.e-21*(i+1)

# transfer value to cell indexed array
for k in range(nz):
    for j in range(ny):
        for i in range(nx):
            index = i + j*nx + k*nx*ny
            cell_indexed_array[index] = ijk_array[i][j][k]
            
# write the cell indexed dataset
dataset_name = 'bravo'
h5dset = h5file.create_dataset(dataset_name, data=cell_indexed_array)
            
# FOR ANISOTROPIC PERMEABILITY ################################################
ijk_array_x = ijk_array.copy()
ijk_array_y = ijk_array.copy()
ijk_array_z = ijk_array.copy()
# set values in ijk_array
for k in range(nz):
    for j in range(ny):
        for i in range(nx):
            ijk_array_x[i][j][k] = 2.e-12+1.e-15*(k+1)+1.e-18*(j+1)+1.e-21*(i+1)
            ijk_array_y[i][j][k] = 3.e-12+1.e-15*(k+1)+1.e-18*(j+1)+1.e-21*(i+1)
            ijk_array_z[i][j][k] = 4.e-12+1.e-15*(k+1)+1.e-18*(j+1)+1.e-21*(i+1)

cell_indexed_array_x = cell_indexed_array.copy()
cell_indexed_array_y = cell_indexed_array.copy()
cell_indexed_array_z = cell_indexed_array.copy()
# transfer value to cell indexed array
for k in range(nz):
    for j in range(ny):
        for i in range(nx):
            index = i + j*nx + k*nx*ny
            cell_indexed_array_x[index] = ijk_array_x[i][j][k]
            cell_indexed_array_y[index] = ijk_array_y[i][j][k]
            cell_indexed_array_z[index] = ijk_array_z[i][j][k]
            
# write the cell indexed dataset
dataset_name = 'delta'
h5dset = h5file.create_dataset(dataset_name, data=cell_indexed_array_x)
dataset_name = 'echo'
h5dset = h5file.create_dataset(dataset_name, data=cell_indexed_array_y)
dataset_name = 'foxtrot'
h5dset = h5file.create_dataset(dataset_name, data=cell_indexed_array_z)

# create a cell id array
cell_id_array = numpy.zeros((n),numpy.int32)  
for i in range(n):
  cell_id_array[i] = i+1 # add 1 for one-based indexing in PFLOTRAN
  
# write the cell id dataset
dataset_name = 'Cell Ids'
h5dset = h5file.create_dataset(dataset_name, data=cell_id_array)

h5file.close()
print('done creating cell indexed dataset')
  
'''