## HOW TO USE
## python3 organizeResults <FOLDER_WITH_PFT_FILES>

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
ax1 = plt.subplot2grid((2,3),(0,0),rowspan=1,colspan=2)
ax2 = plt.subplot2grid((2,3),(1,0),rowspan=1,colspan=2,sharex=ax1)

# Number of colors to plots
cmap = get_cmap(len(listdir(FOLDER)))

i=0
for f in listdir(FOLDER):
  ObservationPoint = np.genfromtxt(FOLDER+"/"+f, delimiter=',', skip_header=1)
  Cmax = 1.0E-20
  Cnorm = ObservationPoint[:,VAQ_COL_ID]/Cmax
  Time = ObservationPoint[:,TIME_COL_ID]
  
  if "Public" in f:
    ax1.plot(Time,Cnorm,c=cmap(i),lw=3,label=f[:-17])
  elif "Domestic" in f:
    ax2.plot(Time,Cnorm,c=cmap(i),lw=3,label=f[:-19])
  
  i+=1

LegendTitle="$\\dfrac{[V_{(aq)}]}{[V_{(aq)}]_0}$"
ax1.set_yscale("log")
ax1.legend(loc='center left', bbox_to_anchor=(1.2, 0.5),title=LegendTitle + " Public")

ax2.set_yscale("log")
ax2.set_xlabel("Time [d]",fontsize="large")
ax2.legend(loc='center left', bbox_to_anchor=(1.2, 0.5),title=LegendTitle + " Domestic")

plt.setp(ax1.get_xticklabels(), visible=False)

plt.subplots_adjust(wspace=0.0, hspace=0.1)

plt.savefig("./break2.png",transparent=False)