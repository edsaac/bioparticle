#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact_manual
import ipywidgets as wd
from os import system

## New functions 
import PFLOTRAN as PFLO

## Global variables
L = 50 #cm
ConcentrationAtInlet = 1.66E-16 #mol/L
InjectTimeInPoreVol = 1.04

## Initialize PFLOTRAN model
ColumnModel = PFLO.Model()
TemplateFile = "templatePFLO.tpl"

# Parameters with a fixed value:
Porosity     = PFLO.Var(tag="<porosity>",value=0.37,units="adim")
FlowVelocity = PFLO.Var(tag="<darcyVel>",value=0.7585,units="cm/h")

# Parameters with a fixed value but calculated from other parameters
ElutionTime  = PFLO.Var(tag="<elutionTime>",\
                        value=3600*L*InjectTimeInPoreVol*Porosity.get_value()/FlowVelocity.get_value(),\
                        units="s")
EndTime      = PFLO.Var(tag="<endTime>",\
                        value=10.*InjectTimeInPoreVol,\
                        units="d")

# Parameters whose values are set by Ostrich Calibrator:
LongDisp     = PFLO.Var(tag="<longDisp>",units="cm")
RateAttachment = PFLO.Var(tag="<katt>",units="1/h")
RateDetachment = PFLO.Var(tag="<kdet>",units="1/h")
RateDecayAqueo = PFLO.Var(tag="<decayAq>",units="1/h")
RateDecayImmob = PFLO.Var(tag="<decayIm>",units="1/h")

# List of parameters this scrips controls
thingsThisScriptControls = [
    Porosity,
    FlowVelocity,
    ElutionTime,
    EndTime]
thingsOstrichWillControl = [
    LongDisp,
    RateAttachment,
    RateDetachment,
    RateDecayAqueo,
    RateDecayImmob
]

# Function for running the model
ColumnModel.cloneTemplate(TemplateFile)
for parameter in thingsThisScriptControls:
  parameter.replaceTag()
ColumnModel.runModel()
ColumnModel.fixTecFile()

# Convert results in PV and C/C0 units
def postprocessResults():
  ResultsFile = "./pflotran-obs-0.tec"
  ObservationPoint = np.loadtxt(ResultsFile,delimiter=",",skiprows=1)
  Cnorm = ObservationPoint[:,3]/ConcentrationAtInlet
  TimeInPoreVolumes = 24.0 * ObservationPoint[:,0] * FlowVelocity.get_value()/(L*Porosity.get_value())
  return TimeInPoreVolumes, Cnorm

# Print file with only the observation points

whereInPV = [
  0.763636363636364,
  0.872727272727273,
  0.927272727272727,
  0.981818181818182,
  1.05454545454545,
  1.27272727272727,
  1.49090909090909,
  1.8,
  1.98181818181818,
  2.09090909090909,
  2.16363636363636,
  2.34545454545455,
  2.47272727272727,
  2.72727272727273,
  3,
  3.27272727272727,
  3.54545454545455,
  3.94545454545454,
  4.65454545454545,
  5,
  5.34545454545455
 ]

ObservationsRelC = [
  9.456536E-05,
  4.677454E-02,
  1.232629E-01,
  3.756760E-01,
  8.153598E-01,
  8.964703E-01,
  8.945760E-01,
  8.094882E-01,
  5.483072E-01,
  1.553088E-01,
  6.485487E-02,
  5.735159E-03,
  3.527632E-03,
  3.042661E-03,
  1.466614E-03,
  9.925363E-04,
  2.610061E-03,
  7.738392E-04,
  7.685375E-04,
  6.011009E-04,
  9.267583E-04
]

# Build results file 
## PV relC

PV, normC = postprocessResults()
valuesAtGivenPV = np.interp(whereInPV,PV,normC)
f = open("ResultsFile.txt",mode='w+')
f.write("PoreVolume RelativeConcentration\n")
for i in range(len(valuesAtGivenPV)):
  pv = whereInPV[i]
  c  = np.log10(valuesAtGivenPV[i])
  f.write("{:.5E}".format(pv) + \
          " " + \
          "{:.5E}".format(c) + "\n")
f.close()

# Plot the final breakthrough curve
plt.figure(figsize=(8,5),facecolor="white")
ax1 = plt.subplot(1,1,1)
ax1.plot(PV,normC,lw=2,c="black",label="Model")
ax1.set_yscale("symlog",\
      linthresh=1.0E-6,subs=[1,2,3,4,5,6,7,8,9])
ax1.set_ylim([-1.0E-7,1.15])
ax1.set_xlim([0,6])
ax1.set_xlabel("Pore Volume [$-$]",fontsize="large")
ax1.axvline(x=InjectTimeInPoreVol,ls="dotted",c="gray",lw=1)
ax1.axhspan(ymin=-1.0E-7,ymax=1.0E-6,facecolor="pink",alpha=0.2)
ax1.scatter(whereInPV,ObservationsRelC,marker="o",label="Observations")
ax1.legend()

## Performance metrics
deltaC = np.log10(valuesAtGivenPV)-np.log10(ObservationsRelC)
RMSE = np.sqrt(np.mean(np.square(deltaC)))
NSE  = 1 - np.sum(np.square(deltaC))/np.sum(np.square(np.log10(ObservationsRelC)-np.mean(np.log10(ObservationsRelC))))

ax1.text(5.5,5.0E-3,"RMSE = {:.2E}\n NSE = {:.3f}".format(RMSE,NSE),\
    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.25),\
    horizontalalignment='right')

import time
# clk_id for System-wide real-time clock 
timeId = int(time.clock_gettime(time.CLOCK_REALTIME))
plt.savefig("./Result_{}.png".format(timeId))
