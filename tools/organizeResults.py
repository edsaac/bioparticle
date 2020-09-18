import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from os import system
import sys

FILE = str(sys.argv[1])

try:
	CLEAN = "clean" in str(sys.argv[2])
except IndexError:
	CLEAN = False

if CLEAN:
	system("sed -i 's/,/  /g' " + FILE)
	system("head -3 " + FILE)
	system("rm -r VTK")
	system("mkdir VTK")
	system("mv *.vtk ./VTK/")
	system("rm *.out")

ObservationPoint = read_csv(FILE,sep="  ",engine="python")

Cmax = max(ObservationPoint["\"Total Vaq [M] Obs__PointOutflow (100) (0.025 0.025 0.498)\""])
Cnorm = ObservationPoint["\"Total Vaq [M] Obs__PointOutflow (100) (0.025 0.025 0.498)\""]/Cmax
Time = ObservationPoint["\"Time [d]\""]

Legend=["$\\dfrac{[V_{(aq)}]}{[V_{(aq)}]_0}$"]

fig = plt.figure(figsize=(5,4),facecolor="white")
ax1 = plt.subplot(1,1,1)
ax1.plot(Time,Cnorm,c="violet",lw=3,label=Legend[0])
ax1.set_ylim([1.0E-3,1.2])
ax1.set_xlim([0,10])

ax1.set_yscale("log")

#ax1.set_ylabel(Legend[0],fontsize="large",rotation=0)
ax1.set_xlabel("Time [$a$]",fontsize="large")
ax1.legend(fontsize="large")
plt.savefig("./breaktrough.png",transparent=True)