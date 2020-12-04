###############################################################
#  _     _                        _   _      _
# | |__ (_) ___  _ __   __ _ _ __| |_(_) ___| | ___
# | '_ \| |/ _ \| '_ \ / _` | '__| __| |/ __| |/ _ \
# | |_) | | (_) | |_) | (_| | |  | |_| | (__| |  __/
# |_.__/|_|\___/| .__/ \__,_|_|   \__|_|\___|_|\___|
#               |_|
# 
###############################################################

import numpy as np
import matplotlib.pyplot as plt
from os import system
import sys
import ipywidgets as wd

###############################################################
# Variables have a tag, a value and units
###############################################################
class Var:
  ## constructor
  def __init__(self, tag, value=None, units=None, slider=None):
    self.tag = tag
    self.value = value
    self.units = units
    if slider is None :
      self.slider = wd.FloatLogSlider(
        value=10,
        base=10,
        min=-10, # max exponent of base
        max=1, # min exponent of base
        step=0.2, # exponent step
        description = self.tag
      )
    else :
      self.slider = slider
  ## get methods
  def get_tag(self):
    return(self.tag)
  def get_value(self):
    return(self.value)
  def get_strValue(self):
    return("{:.2E}".format(self.value))
  def get_units(self):
    return(self.units)
  def get_slider(self):
    return(self.slider)

  ## set methods
  def set_tag(self,tag):
    self.tag = tag
    return None
  def set_value(self,value):
    self.value = value
    return None
  def set_units(self,units):
    self.units = units
    return None
  def set_slider(self,slider):
    self.slider = slider
    return None
  ## 
  def replaceTag(self,pflotranFile="./pflotran.in"):
    if self.value is None:
      print("Object has no value asigned :/ \n Try set_value()")
      return None
    else:
      C = "sed -i 's/" + self.tag + "/"\
        +'{:.3E}'.format(self.value)\
        + "/g' " + pflotranFile
      system(C)
      return None
        
###############################################################
# A model has an input file, a path to the executable
###############################################################
class Model:
  ## constructor
  def __init__(\
    self,\
    execPath = "$PFLOTRAN_DIR/src/pflotran/pflotran",\
    runFile="./pflotran.in"):
    self.execPath = execPath
    self.runFile = runFile
  ## get methods
  def get_execPath(self):
    return(self.execPath)
  def get_runFile(self):
    return(self.runFile)
  ## set methods
  def set_execPath(self,execPath):
    self.execPath = execPath
    return None
  def set_runFile(self,runFile):
    self.runFile = runFile
    return None
  ## File management
  def cloneTemplate(self,TemplateFile):
    system("cp " + TemplateFile + " " + self.runFile)
    return None
  def runModel(self):
    system(self.execPath + " -pflotranin " + self.runFile)
    #system("./miscellaneous/PFT2CSV.sh " + self.runFile)
    return None
  def fixTecFile(self,outputFile="pflotran-obs-0.tec"):
    C = '''
      NCOMMAS=$(head -1 $file | grep -o '"' | wc -l)
      if [ $NCOMMAS -gt 0 ]
        then
        sed -i 's/^  //g' $file
        sed -i '1s/^ //g' $file
        sed -i '1s/"//g' $file
        sed -i 's/  /,/g' $file
        echo "FIXED FILE"
      else
        echo "NOTHING DONE"
      fi
    '''
    system("file=" + outputFile + "; " + C)
  


## Non-dimensional numbers
def DamkII(K,A,U,L,asString=False):
  DaII = (L*L*K)/(A*U)
  if asString:
    return "{:.1E}".format(DaII)
  else:
    return DaII

def Peclet(A,L,U,asString=False):
  Pe = (L*U)/(A*U)
  if asString:
    return "{:.1E}".format(Pe)
  else:
    return Pe


# def plotResults(U,pH,IS,PV,kATT,kDET,dAq,dIm,alpha):
#   FILE = current_folder+"/pflotran-obs-0.tec"

#   textBoxpH = "pH = {:n}".format(pH)\
#     + "\nIS = {:n}".format(IS)
  
#   textBoxKin = \
#     "$k_{\\rm att}$"+" = {:.4f}".for  # ## Plot log-scale
  # ax1 = plt.subplot(1,2,1)
  # ax1.plot(TimeInPoreVolumes,Cnorm,c="purple",lw=3)
  # ax1.set_yscale("symlog",\
  #   linthresh=1.0E-6,subs=[1,2,3,4,5,6,7,8,9])
  # ax1.set_ylim([-1.0E-7,1.15])
  # ax1.set_xlim([0,10])
  # ax1.set_xlabel("Pore Volume [$-$]",fontsize="large")
  # ax1.axvline(x=PV,ls="dotted",c="gray",lw=1)
  # ax1.axhspan(ymin=-1.0E-7,ymax=1.0E-6,facecolor="pink",alpha=0.2)
  # ## Rate values
  # ax1.text(9.5,5.0E-5,textBoxKin,\
  #   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),\
  #   horizontalalignment='right')
  # ## Case pH/IS
  # ax1.text(9.0,1.0E-1,textBoxpH,\
  #   bbox=dict(boxstyle='round', facecolor='purple', alpha=0.15),\
  #   horizontalalignment='right')

  # ## Plot linear-scale
  # ax2 = plt.subplot(1,2,2)
  # ax2.plot(TimeInPoreVolumes,Cnorm,c="purple",lw=3,label=Legend[0])
  # ax2.set_ylim([-1.0E-2,1.02])
  # ax2.set_xlim([0,10])
  # ax2.set_xlabel("Pore Volume [$-$]",fontsize="large")
  # ax2.axvline(x=PV,ls="dotted",c="gray",lw=1)
  # ax2.legend(fontsize="large",loc="upper right")
  # ## Péclet and Damköhler numbers
  # ax2.text(9.5,0.1,textBoxDimensionless,\
  #   bbox=dict(boxstyle='round', facecolor='purple', alpha=0.15),\
  #   horizontalalignment='right')
  
  # plt.tight_layout()  
  # FIGPATH = current_folder + "/" + "CASE_" + current_folder[7:10] + ".png"
  # #plt.show()
  # plt.savefig(FIGPATH,transparent=False)mat(kATT) + " h$^{-1}$" +"\n" + \
#     "$k_{\\rm det}$"+" = {:.4f}".format(kDET) + " h$^{-1}$" +"\n" + \
#     "$\lambda_{\\rm aq}$"+" = {:.4f}".format(dAq)+ " h$^{-1}$" +"\n" + \
#     "$\lambda_{\\rm im}$"+" = {:.4f}".format(dIm)+ " h$^{-1}$" +"\n" + \
#     "$\\alpha_{\\rm L}$"+" = {:.4f}".format(alpha)+ " cm "
  
#   textBoxDimensionless = "Damköhler(II) = $\\dfrac{\\rm reaction}{\\rm dispersion}$"+"\n" +\
#     "Da$^{\\rm att}$"+" = {:.1E}".format(DaII(kATT,alpha,U)) +"\n" +\
#     "Da$^{\\rm det}$"+" = {:.1E}".format(DaII(kDET,alpha,U)) +"\n" +\
#     "Da$^{\\rm λaq}$"+" = {:.1E}".format(DaII(dAq, alpha,U)) +"\n" +\
#     "Da$^{\\rm λim}$"+" = {:.1E}".format(DaII(dIm, alpha,U)) +"\n\n" +\
#     "Péclet = $\\dfrac{\\rm advection}{\\rm dispersion}$"+"\n" +\
#     "P$_{\\rm é}$"+" = {:.1E}".format(Peclet(alpha))

  
#   #system("rm " + current_folder +"/*.out")
  
#   ObservationPoint = np.loadtxt(FILE,delimiter=",",skiprows=1)
#   Cnorm = ObservationPoint[:,3]/ConcentrationAtInlet
#   TimeInPoreVolumes = ObservationPoint[:,0] * (U*24.)/ColumnLenght
  
#   Legend=["$\\dfrac{[V_{(aq)}]}{[V_{(aq)}]_0}$"]
#   plt.figure(figsize=(10,4),facecolor="white")
  
  # ## Plot log-scale
  # ax1 = plt.subplot(1,2,1)
  # ax1.plot(TimeInPoreVolumes,Cnorm,c="purple",lw=3)
  # ax1.set_yscale("symlog",\
  #   linthresh=1.0E-6,subs=[1,2,3,4,5,6,7,8,9])
  # ax1.set_ylim([-1.0E-7,1.15])
  # ax1.set_xlim([0,10])
  # ax1.set_xlabel("Pore Volume [$-$]",fontsize="large")
  # ax1.axvline(x=PV,ls="dotted",c="gray",lw=1)
  # ax1.axhspan(ymin=-1.0E-7,ymax=1.0E-6,facecolor="pink",alpha=0.2)
  # ## Rate values
  # ax1.text(9.5,5.0E-5,textBoxKin,\
  #   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),\
  #   horizontalalignment='right')
  # ## Case pH/IS
  # ax1.text(9.0,1.0E-1,textBoxpH,\
  #   bbox=dict(boxstyle='round', facecolor='purple', alpha=0.15),\
  #   horizontalalignment='right')

  # ## Plot linear-scale
  # ax2 = plt.subplot(1,2,2)
  # ax2.plot(TimeInPoreVolumes,Cnorm,c="purple",lw=3,label=Legend[0])
  # ax2.set_ylim([-1.0E-2,1.02])
  # ax2.set_xlim([0,10])
  # ax2.set_xlabel("Pore Volume [$-$]",fontsize="large")
  # ax2.axvline(x=PV,ls="dotted",c="gray",lw=1)
  # ax2.legend(fontsize="large",loc="upper right")
  # ## Péclet and Damköhler numbers
  # ax2.text(9.5,0.1,textBoxDimensionless,\
  #   bbox=dict(boxstyle='round', facecolor='purple', alpha=0.15),\
  #   horizontalalignment='right')
  
  # plt.tight_layout()  
  # FIGPATH = current_folder + "/" + "CASE_" + current_folder[7:10] + ".png"
  # #plt.show()
  # plt.savefig(FIGPATH,transparent=False)

# ## Tags dictionary for variables in input file
# tagsReplaceable =	{
#   "Porosity"  : "<porosity>",
#   "DarcyVel"  : "<darcyVel>",     # q = u*porosity
#   "CleanTime" : "<elutionTime>",  # t @ C0 = 0
#   "FinalTime" : "<endTime>",      # @ 10 pore volumes
#   "AttachRate": "<katt>",
#   "DetachRate": "<kdet>",
#   "DecayAq"   : "<decayAq>",
#   "DecayIm"   : "<decayIm>",
#   "LongDisp"  : "<longDisp>"
# }

# ## Tags dictionary for other parameters
# tagsAccesory =	{
#   "FlowVel"   : "poreWaterVel",
#   "PoreVol"   : "poreVolume",
#   "pH"        : "pH",
#   "IonicStr"  : "IS"
# }

# ## Path to PFLOTRAN executable
# PFLOTRAN_path = "$PFLOTRAN_DIR/src/pflotran/pflotran "

# ## Table with the set of parameters
# try:
# 	parameters_file = str(sys.argv[1])
# except IndexError:
# 	sys.exit("Parameters file not defined :(")

# setParameters = read_csv(parameters_file)
# total_rows = setParameters.shape[0]

# ## Template for the PFLOTRAN input file
# try:
# 	template_file = str(sys.argv[2])
# except IndexError:
# 	sys.exit("Template file not found :(")

# ## Run cases?
# try:
# 	shouldRunPFLOTRAN = "-run" in str(sys.argv[3])
# except IndexError:
# 	shouldRunPFLOTRAN = False

# ## Delete previous cases
# system("rm -rf CASE*")

# ## Row in the set of parameters table = case to be run
# for i in range(total_rows):
# #for i in range(1):
  
#   ## Create a folder for the case
#   current_folder = "./CASE_" + "{0:03}".format(i+1)
#   system("mkdir " + current_folder)
  
#   ## Copy template input file to folder
#   system("cp " + template_file + " " + current_folder+"/pflotran.in")
#   current_file = current_folder + "/pflotran.in" 
 
#   ## Replace tags for values in case
#   for current_tag in tagsReplaceable:
#     COMM = "sed -i 's/" + tagsReplaceable[current_tag] + "/"\
#       +'{:.3E}'.format(setParameters.loc[i,tagsReplaceable[current_tag]])\
#       + "/g' " + current_file
#     system(COMM)
  
#   ## Run PFLOTRAN in that case
#   if shouldRunPFLOTRAN:
#     #print(PFLOTRAN_path + "-pflotranin " + current_file)
#     system(PFLOTRAN_path + "-pflotranin " + current_file)
#     #system("python3 ./miscellaneous/organizeResults.py " + current_folder + "/pflotran-obs-0.tec -clean")
#     current_U = setParameters.loc[i,tagsAccesory["FlowVel"]]
#     current_pH = setParameters.loc[i,tagsAccesory["pH"]]
#     current_IS = setParameters.loc[i,tagsAccesory["IonicStr"]]
#     current_PV = setParameters.loc[i,tagsAccesory["PoreVol"]]

#     current_kAtt = setParameters.loc[i,tagsAccesory["PoreVol"]]
#     current_k = setParameters.loc[i,tagsAccesory["PoreVol"]]
#     current_PV = setParameters.loc[i,tagsAccesory["PoreVol"]]
#     current_PV = setParameters.loc[i,tagsAccesory["PoreVol"]]
#     #input("Press Enter to continue...")
#     plotResults(current_U,current_pH,current_IS,current_PV,\
#       setParameters.loc[i,tagsReplaceable["AttachRate"]],\
#       setParameters.loc[i,tagsReplaceable["DetachRate"]],\
#       setParameters.loc[i,tagsReplaceable["DecayAq"]],\
#       setParameters.loc[i,tagsReplaceable["DecayIm"]],\
#       setParameters.loc[i,tagsReplaceable["LongDisp"]])
#     #input("Press Enter to continue...")
# system("rm -r pictures ; mkdir pictures")
# system("cp CASE**/*.png ./pictures/")