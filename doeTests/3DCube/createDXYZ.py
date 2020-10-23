import numpy as np
import matplotlib.pyplot as plt
from os import system
import sys

L = 10.0   #Domain lenght
R = -10   #Total expansion ratio
N = 12     #Number of elements
bump=True

if abs(R) < 1e-10:
  R = 1

if bump:
  L = L/2.0
  N = int(N/2.0)

# Cell-to-cell ratio
K = np.power(np.abs(R),1/(N-1))
KPow = np.power(np.ones(N)*K,np.arange(0,N,1,dtype="int16"))

# Smallest element
D1 = L/(np.sum(KPow))

# Array of distances
Distances = np.ones(N)
Distances[0] = D1
for i in range(1,N):
	Distances[i] = Distances[i-1] * K

if R < 0:
	Distances = np.flip(Distances)

print(Distances)

if bump:
	Definitive = np.concatenate((Distances,np.flip(Distances)))
	plotas=np.ones(2*N)
else:
	Definitive = Distances
	plotas=np.ones(N)

print(Definitive)
print(np.cumsum(Definitive))

Formatted = ""
for i in range(len(Definitive)):
	Formatted+="{:.3E} ".format(Definitive[i])
	if i % 6 == 5:
		Formatted+="\n"
print(Formatted)

plt.plot(plotas,np.cumsum(Definitive),marker="o")
plt.show()
