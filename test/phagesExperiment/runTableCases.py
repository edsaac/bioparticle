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
# $ python3 runTableCases.py [CASES.CSV] [TEMPLATE.IN] -run
# 
# Where:
#   - [CASES.CSV] path to csv file with the list of 
#     parameters and the corresponding tags
#   - [TEMPLATE.IN] input file template for PFLOTRAN and 
#     the corresponding tags
#   - [shouldRunPFLOTRAN = "-run"]
#
###############################################################

import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from os import system
import sys

## Global variables
ColumnLenght = 50.0
ConcentrationAtInlet = 1.66E-16

## Non-dimensional numbers
def DaII(K,A,U,L=ColumnLenght):
  return (L*L*K)/(A*U)

def Peclet(A,L=ColumnLenght):
  return L/A

def plotResults(U,pH,IS,PV,kATT,kDET,dAq,dIm,alpha):
  FILE = current_folder+"/pflotran-obs-0.tec"

  textBoxpH = "pH = {:n}".format(pH)\
    + "\nIS = {:n}".format(IS)
  
  textBoxKin = \
    "$k_{\\rm att}$"+" = {:.4f}".format(kATT) + " h$^{-1}$" +"\n" + \
    "$k_{\\rm det}$"+" = {:.4f}".format(kDET) + " h$^{-1}$" +"\n" + \
    "$\lambda_{\\rm aq}$"+" = {:.4f}".format(dAq)+ " h$^{-1}$" +"\n" + \
    "$\lambda_{\\rm im}$"+" = {:.4f}".format(dIm)+ " h$^{-1}$" +"\n" + \
    "$\\alpha_{\\rm L}$"+" = {:.4f}".format(alpha)+ " cm "
  
  textBoxDimensionless = "Damköhler(II) = $\\dfrac{\\rm reaction}{\\rm dispersion}$"+"\n" +\
    "Da$^{\\rm att}$"+" = {:.1E}".format(DaII(kATT,alpha,U)) +"\n" +\
    "Da$^{\\rm det}$"+" = {:.1E}".format(DaII(kDET,alpha,U)) +"\n" +\
    "Da$^{\\rm λaq}$"+" = {:.1E}".format(DaII(dAq, alpha,U)) +"\n" +\
    "Da$^{\\rm λim}$"+" = {:.1E}".format(DaII(dIm, alpha,U)) +"\n\n" +\
    "Péclet = $\\dfrac{\\rm advection}{\\rm dispersion}$"+"\n" +\
    "P$_{\\rm é}$"+" = {:.1E}".format(Peclet(alpha))

  system("./miscellaneous/PFT2CSV.sh " + FILE)
  #system("rm " + current_folder +"/*.out")
  
  ObservationPoint = np.loadtxt(FILE,delimiter=",",skiprows=1)
  Cnorm = ObservationPoint[:,1]/ConcentrationAtInlet
  TimeInPoreVolumes = ObservationPoint[:,0] * U*24./(ColumnLenght)
  
  Legend=["$\\dfrac{[V_{(aq)}]}{[V_{(aq)}]_0}$"]
  plt.figure(figsize=(10,4),facecolor="white")
  
  ## Plot log-scale
  ax1 = plt.subplot(1,2,1)
  ax1.plot(TimeInPoreVolumes,Cnorm,c="purple",lw=3)
  ax1.set_yscale("symlog",\
    linthresh=1.0E-6,subs=[1,2,3,4,5,6,7,8,9])
  ax1.set_ylim([-1.0E-7,1.15])
  ax1.set_xlim([0,10])
  ax1.set_xlabel("Pore Volume [$-$]",fontsize="large")
  ax1.axvline(x=PV,ls="dotted",c="gray",lw=1)
  ax1.axhspan(ymin=-1.0E-7,ymax=1.0E-6,facecolor="pink",alpha=0.2)
  ## Rate values
  ax1.text(9.5,5.0E-5,textBoxKin,\
    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),\
    horizontalalignment='right')
  ## Case pH/IS
  ax1.text(9.0,1.0E-1,textBoxpH,\
    bbox=dict(boxstyle='round', facecolor='purple', alpha=0.15),\
    horizontalalignment='right')

  ## Plot linear-scale
  ax2 = plt.subplot(1,2,2)
  ax2.plot(TimeInPoreVolumes,Cnorm,c="purple",lw=3,label=Legend[0])
  ax2.set_ylim([-1.0E-2,1.02])
  ax2.set_xlim([0,10])
  ax2.set_xlabel("Pore Volume [$-$]",fontsize="large")
  ax2.axvline(x=PV,ls="dotted",c="gray",lw=1)
  ax2.legend(fontsize="large",loc="upper right")
  ## Péclet and Damköhler numbers
  ax2.text(9.5,0.1,textBoxDimensionless,\
    bbox=dict(boxstyle='round', facecolor='purple', alpha=0.15),\
    horizontalalignment='right')
  
  plt.tight_layout()  
  FIGPATH = current_folder + "/" + "CASE_" + current_folder[7:10] + ".png"
  #plt.show()
  plt.savefig(FIGPATH,transparent=False)

## Tags dictionary for variables in input file
tagsReplaceable =	{
  "Porosity"  : "<porosity>",
  "DarcyVel"  : "<darcyVel>",     # q = u*porosity
  "CleanTime" : "<elutionTime>",  # t @ C0 = 0
  "FinalTime" : "<endTime>",      # @ 10 pore volumes
  "AttachRate": "<katt>",
  "DetachRate": "<kdet>",
  "DecayAq"   : "<decayAq>",
  "DecayIm"   : "<decayIm>",
  "LongDisp"  : "<longDisp>"
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

    #Porosity = setParameters.loc[i,tagsReplaceable["Porosity"]]
    
    #input("Press Enter to continue...")
    plotResults(current_U,current_pH,current_IS,current_PV,\
      setParameters.loc[i,tagsReplaceable["AttachRate"]],\
      setParameters.loc[i,tagsReplaceable["DetachRate"]],\
      setParameters.loc[i,tagsReplaceable["DecayAq"]],\
      setParameters.loc[i,tagsReplaceable["DecayIm"]],\
      setParameters.loc[i,tagsReplaceable["LongDisp"]])
    #input("Press Enter to continue...")
system("rm -r pictures ; mkdir pictures")
system("cp CASE**/*.png ./pictures/")