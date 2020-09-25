import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from os import system
import sys

def plotResults(U,pH,IS,PV,kATT,kDET,dAq,dIm):
  FILE = current_folder+"/pflotran-obs-0.tec"

  textBoxpH = "pH = {:n}".format(pH)\
    + "\nIS = {:n}".format(IS)

  textBoxKin = "$k_{\\rm att}$"+" = {:.4f}".format(kATT)\
    + "\n$k_{\\rm det}$"+" = {:.4f}".format(kDET)\
    + "\n$\lambda_{\\rm aq}$"+" = {:.4f}".format(dAq)\
    + "\n$\lambda_{\\rm im}$"+" = {:.4f}".format(dIm)\


  system("sed -i 's/,/  /g' " + FILE)
  system("rm " + current_folder +"/*.out")

  ObservationPoint = read_csv(FILE,sep="  ",engine="python")
  Cnorm = ObservationPoint["\"Total Vaq [M] Obs__PointOutflow (100) (0.025 0.025 0.498)\""]/ConcentrationAtInlet
  TimeInPoreVolumes = ObservationPoint["\"Time [d]\""] * (U*24.)/ColumnLenght
  
  Legend=["$\\dfrac{[V_{(aq)}]}{[V_{(aq)}]_0}$"]
  fig = plt.figure(figsize=(10,4),facecolor="white")
  
  ## Plot log-scale
  ax1 = plt.subplot(1,2,1)
  ax1.plot(TimeInPoreVolumes,Cnorm,c="black",lw=3)
  ax1.set_yscale("symlog",\
    linthreshy=1.0E-6,subsy=[1,2,3,4,5,6,7,8,9])
  ax1.set_ylim([-1.0E-7,1.15])
  ax1.set_xlim([0,10])
  ax1.set_xlabel("Pore Volume [$-$]",fontsize="large")
  ax1.axvline(x=PV,ls="dotted",c="gray",lw=1)
  ax1.text(9.0,1.0E-3,textBoxKin,\
    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),\
    horizontalalignment='right')

  ## Plot linear-scale
  ax2 = plt.subplot(1,2,2)
  ax2.plot(TimeInPoreVolumes,Cnorm,c="black",lw=3,label=Legend[0])
  ax2.set_ylim([-1.0E-2,1.02])
  ax2.set_xlim([0,10])
  ax2.set_xlabel("Pore Volume [$-$]",fontsize="large")
  ax1.axvline(x=PV,ls="dotted",c="gray",lw=1)
  ax2.legend(fontsize="large",loc="upper right")
  ax2.text(9.0,0.6,textBoxpH,\
    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),\
    horizontalalignment='right')

  plt.savefig(current_folder + "/breakthrough.png",transparent=False)

## Global variables
ColumnLenght = 50.0
ConcentrationAtInlet = 1.66E-16

## Tags dictionary for variables in input file
tagsReplaceable =	{
  "Porosity"  : "<porosity>",
  "DarcyVel"  : "<darcyVel>",     # q = u*porosity
  "CleanTime" : "<elutionTime>",  # t @ C0 = 0
  "FinalTime" : "<endTime>",      # @ 10 pore volumes
  "AttachRate": "<katt>",
  "DetachRate": "<kdet>",
  "DecayAq"   : "<decayAq>",
  "DecayIm"   : "<decayIm>"
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

setParameters = read_csv(parameters_file)
total_rows = setParameters.shape[0]

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

## Delete previous cases
system("rm -rf CASE*")

## Row in the set of parameters table = case to be run
for i in range(total_rows):
#for i in range(1):
  
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
    #print(PFLOTRAN_path + "-pflotranin " + current_file)
    system(PFLOTRAN_path + "-pflotranin " + current_file)
    #system("python3 ./miscellaneous/organizeResults.py " + current_folder + "/pflotran-obs-0.tec -clean")
    current_U = setParameters.loc[i,tagsAccesory["FlowVel"]]
    current_pH = setParameters.loc[i,tagsAccesory["pH"]]
    current_IS = setParameters.loc[i,tagsAccesory["IonicStr"]]
    current_PV = setParameters.loc[i,tagsAccesory["PoreVol"]]

    current_kAtt = setParameters.loc[i,tagsAccesory["PoreVol"]]
    current_k = setParameters.loc[i,tagsAccesory["PoreVol"]]
    current_PV = setParameters.loc[i,tagsAccesory["PoreVol"]]
    current_PV = setParameters.loc[i,tagsAccesory["PoreVol"]]

    plotResults(current_U,current_pH,current_IS,current_PV,\
      setParameters.loc[i,tagsReplaceable["AttachRate"]],\
      setParameters.loc[i,tagsReplaceable["DetachRate"]],\
      setParameters.loc[i,tagsReplaceable["DecayAq"]],\
      setParameters.loc[i,tagsReplaceable["DecayIm"]])
    input("Press Enter to continue...")
  