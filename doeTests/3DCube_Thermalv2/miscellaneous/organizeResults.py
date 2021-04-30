## HOW TO USE
## python3 organizeResults <FOLDER_WITH_PFT_FILES>

import numpy as np
import matplotlib.pyplot as plt
from os import system, listdir
import sys

def get_cmap(n, name='tab10'): ## Color map for plots 
  return plt.cm.get_cmap(name, n)

FOLDER = str(sys.argv[1])
VAQ_COL_ID = 8
TIME_COL_ID = 0

# Fix those weird PFT headers
system("./PFT2CSV.sh "+ FOLDER)
fig = plt.figure(figsize=(8,5),facecolor="white")
ax1 = plt.subplot2grid((2,2),(0,0),rowspan=2,colspan=2)
#ax2 = plt.subplot2grid((2,3),(1,0),rowspan=1,colspan=2,sharex=ax1)

# Number of colors to plots
cmap = get_cmap(len(listdir(FOLDER)))

i=0
for f in listdir(FOLDER):
  if "NoTemp" in f:
    VAQ_COL_ID = 3
    LS = 'dashed'
    COLOR = 'black'
  else:
    VAQ_COL_ID = 8
    LS = 'solid'
    COLOR = cmap(i)
  
  ObservationPoint = np.genfromtxt(FOLDER+"/"+f, delimiter=',', skip_header=1)
  Cmax = 1.0E-20
  Cnorm = ObservationPoint[:,VAQ_COL_ID]/Cmax
  Time = ObservationPoint[:,TIME_COL_ID]
  ax1.plot(Time,Cnorm,c=COLOR,lw=3.5,ls=LS,label=f[22:-10])
  i+=1

LegendTitle="$\\dfrac{[V_{(aq)}]}{[V_{(aq)}]_0}$"

ax1.set_yscale("symlog",linthresh=1.0E-6)
ax1.set_ylim([-1.0E-7,1.2])
ax1.axhspan(ymin=-1,ymax=1.0E-6,color="purple",alpha=0.05)
ax1.set_xlabel("Time [d]",fontsize="large")
#ax1.legend(loc='center left', bbox_to_anchor=(1.2, 0.5),title=LegendTitle + " Temperature")
ax1.legend(title=LegendTitle + " Temperature")
plt.tight_layout()
#plt.subplots_adjust(wspace=0.0, hspace=0.1)
plt.savefig("./breakThermal.png",transparent=False)
