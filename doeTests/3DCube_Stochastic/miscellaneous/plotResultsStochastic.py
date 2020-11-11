## HOW TO USE
## python3 plotResultsStochastic.py <FOLDER_WITH_PFT_FILES>

import numpy as np
import matplotlib.pyplot as plt
from os import system, listdir
import sys

def get_cmap(n, name='tab10'): ## Color map for plots 
  return plt.cm.get_cmap(name, n)

FOLDER = str(sys.argv[1])
VAQ_COL_ID = 3
TIME_COL_ID = 0

# Fix those weird PFT headers
system("./PFT2CSV.sh "+ FOLDER)
fig = plt.figure(figsize=(8,5),facecolor="white")
ax1 = plt.subplot2grid((3,3),(0,0),rowspan=3,colspan=3)

# Number of colors to plots
cmap = get_cmap(len(listdir(FOLDER)))

i=0

for f in listdir(FOLDER):
  ObservationPoint = np.genfromtxt(FOLDER+"/"+f, delimiter=',', skip_header=1)
  Cmax = 1.0E-20
  Cnorm = ObservationPoint[:,VAQ_COL_ID]/Cmax
  Time = ObservationPoint[:,TIME_COL_ID]
  
  if i == 0:
    CAcum = np.zeros_like(Cnorm)
  else:
    CAcum += Cnorm
  
  # Plot
  ax1.plot(Time,Cnorm,c="green",lw=1,alpha=0.05)
  i+=1
CAcum = CAcum/i
ax1.plot(Time,CAcum,c="black",lw=1,ls="dashed",\
  label="Mean\nn= %i runs" %i)

LegendTitle="$\\dfrac{[V_{(aq)}]}{[V_{(aq)}]_0}$"
ax1.set_yscale("symlog",linthresh=1.0E-6)
ax1.set_ylim([-1.0E-7,1.2])
ax1.axhspan(ymin=-1,ymax=1.0E-6,color="purple",alpha=0.05)
ax1.legend(loc='lower right')
ax1.set_xlabel("Time [d]",fontsize="large")
ax1.set_ylabel(LegendTitle,fontsize="large")
plt.subplots_adjust(wspace=0.0, hspace=0.1)

plt.savefig("./breakCurve.png",transparent=False)