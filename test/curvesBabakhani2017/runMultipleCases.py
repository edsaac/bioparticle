###############################################################
#  _     _                        _   _      _
# | |__ (_) ___  _ __   __ _ _ __| |_(_) ___| | ___
# | '_ \| |/ _ \| '_ \ / _` | '__| __| |/ __| |/ _ \
# | |_) | | (_) | |_) | (_| | |  | |_| | (__| |  __/
# |_.__/|_|\___/| .__/ \__,_|_|   \__|_|\___|_|\___|
#               |_|
# 
###############################################################
#
# $ python3 runMultipleCases.py <CASES.CSV> <TEMPLATE.IN> -run
# 
# Where:
#   - <CASES.CSV> path to csv file with the list of 
#     parameters and the corresponding tags
#   - <TEMPLATE.IN> input file template for PFLOTRAN and 
#     the corresponding tags
#
###############################################################

import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from os import system
import sys

def get_cmap(n, name='Dark2'): ## Color map for plots 
  return plt.cm.get_cmap(name, n)

def build_label(L1,L2): ## Build text block for label plots
  return "$k_{\\rm att}$"+" = {:.1E}".format(L1) + " $s^{-1}$" +\
    "\n$k_{\\rm det}$"+" = {:.1E}".format(L2) + " $s^{-1}$"

def plotResults(label,counter):
  # Clean text .TEC file for pandas to read
  FILE = current_folder+"/pflotran-obs-0.tec"
  system("sed -i 's/,/  /g' " + FILE)
  system("rm " + current_folder +"/*.out")

  # Read file
  ObservationPoint = read_csv(FILE,sep="  ",engine="python")
  
  # [V(aq)] vector
  TEC_VaqField = "\"Total Vaq [M] Obs__PointOutflow (500) (6.35E-03 6.35E-03 0.255)\""
  Cnorm = ObservationPoint[TEC_VaqField]/ConcentrationAtInlet
  
  # Time (PV) vector
  TimeInPoreVolumes = ObservationPoint["\"Time [s]\""] * (U*100)/ColumnLenght
  
  ## Plot log-scale
  ax1.plot(TimeInPoreVolumes,Cnorm,\
    c=cmap(counter),lw=2,alpha=0.9,\
    label=label) 

  ## Plot linear-scale
  ax2.plot(TimeInPoreVolumes,Cnorm,\
    c=cmap(counter),lw=2,alpha=0.9,\
    label=label) 

def finishPlot():
  #General plot configuration
  ax1.set_yscale("symlog",\
    linthreshy=1.0E-6,subsy=[1,2,3,4,5,6,7,8,9])
  ax1.set_ylim([-1.0E-7,1.15])
  ax1.set_xlim([0,5])
  ax1.set_xlabel("Pore Volume [$-$]",\
    fontsize="large")
  ax1.set_ylabel("$\\dfrac{[V_{(aq)}]}{[V_{(aq)}]_0}$",\
    fontsize="large")
  ax1.axhspan(ymin=-1.0E-7,ymax=1.0E-6,facecolor="pink",alpha=0.2)
  ax1.axvline(x=1.0,ls="dotted",c="gray",lw=0.6)

  ax2.set_ylim([-1.0E-2,1.02])
  ax2.set_xlim([0,5])
  ax2.set_xlabel("Pore Volume [$-$]",\
    fontsize="large")
  ax2.legend(fontsize="small",loc="upper right")
  ax2.axvline(x=1.0,ls="dotted",c="gray",lw=0.6)

  plt.tight_layout()
  plt.savefig(parameters_file[:-4]+".png",transparent=False)

## Global variables
ColumnLenght = 25.5
ConcentrationAtInlet = 1.0E-5

## Tags dictionary for variables in input file
tagsReplaceable =	{
  "Porosity"  : "<porosity>",
  "LongDisp"  : "<longDisp>",
  "DarcyVel"  : "<darcyVel>",     # q = u*porosity
  "CleanTime" : "<elutionTime>",  # t @ C0 = 0
  "FinalTime" : "<endTime>",      # @ 10 pore volumes
  "AttachRate": "<katt>",
  "DetachRate": "<kdet>",
  "DecayAq"   : "<decayAq>",
  "DecayIm"   : "<decayIm>",
  "OutputTimeStep" : "<obsTimeStep>",  # elutionTime/50.
  "ColumnLen" : "<lenColumn>",
  "ColumnDia"	: "<diamColumn>",
  "obsPointX" : "<obsPointX>",
  "obsPointY" : "<obsPointY>",
  "obsPointZ" : "<obsPointZ>"
}

## Tags dictionary for other parameters
tagsAccesory =	{
  "FlowVel"   : "poreWaterVel",
  "PoreVol"   : "poreVolume",
  "pH"        : "pH",
  "IonicStr"  : "IS"
}

## Path to PFLOTRAN executable
PFLOTRAN_path = "$PFLOTRAN_DIR/src/pflotran/pflotran "

## Table with the set of parameters
try:
	parameters_file = str(sys.argv[1])
except IndexError:
	sys.exit("Parameters file not defined :(")

## Template for the PFLOTRAN input file
try:
	template_file = str(sys.argv[2])
except IndexError:
	sys.exit("Template file not found :(")

## Run cases?
try:
	shouldRunPFLOTRAN = "-run" in str(sys.argv[3])
except IndexError:
	shouldRunPFLOTRAN = False

# Read CSV file with cases 
setParameters = read_csv(parameters_file)
total_rows = setParameters.shape[0]
cmap = get_cmap(total_rows)

## Delete previous cases
system("rm -rf CASE*")

## Row in the set of parameters table = case to be run
plt.figure(figsize=(10,4),facecolor="white")
ax1 = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)

for i in range(total_rows):
  
  ## Create a folder for the case
  current_folder = "./CASE_" + "{0:03}".format(i+1)
  system("mkdir " + current_folder)
  
  ## Copy template input file to folder
  system("cp " + template_file + " " + current_folder+"/pflotran.in")
  current_file = current_folder + "/pflotran.in" 
 
  ## Replace tags for values in case
  for current_tag in tagsReplaceable:
    COMM = "sed -i 's/" + tagsReplaceable[current_tag] + "/"\
      +'{:.3E}'.format(setParameters.loc[i,tagsReplaceable[current_tag]])\
      + "/g' " + current_file
    system(COMM)
  
  ## Run PFLOTRAN in that case
  if shouldRunPFLOTRAN:
    
    ## Tell terminal to run PFLOTRAN
    system(PFLOTRAN_path + "-pflotranin " + current_file)
    
    ## Build a label for the results curve
    label = build_label(\
      setParameters.loc[i,tagsReplaceable["AttachRate"]],\
      setParameters.loc[i,tagsReplaceable["DetachRate"]]\
      )

    ## Add curve to plot
    U = setParameters.loc[i,tagsAccesory["FlowVel"]]
    plotResults(label,i)

finishPlot()

