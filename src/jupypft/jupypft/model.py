#!/usr/bin/python3

'''
Module for PFLOTRAN model
<Documentation missing> 
'''  

from os import system
import math

from numpy.core import numeric

class Model:
  '''
  Class for a PFLOTRAN model. 
    
    e.g.
      myModel = Model()
  '''
  __numberOf = 0   # Counter of all instantiated variables 
  __listObjs = []    # List of all instantiated variables 

  def __init__(
    self,
    templateFile,
    description="None provided",
    runFile="./pflotran.in",
    execPath="$PFLOTRAN_DIR/src/pflotran/pflotran",
    folder=".",
    verbose=False
    ):
    '''
    Parameters
    ---------------
    templateFile: string
      The path to the template file that contains all the 
      tags that will be replaced later by values
    runFile: string
      The path of the input file for the PFLOTRAN model
    execPath: string
      The path to the PFLOTRAN executable. Default will
      look for the thing in 
    verbose: bool
      If true, PFLOTRAN std output is shown. 

    )
    '''
    self._templateFile = templateFile
    self._runFile = runFile
    self._description = description
    self._folder = folder
    self._execPath = execPath
    self._verboseAppend = ("2>&1 dev/null","") [verbose]
    
    Model.__numberOf += 1
    Model.__listObjs.append(self)
  
  def __str__(self):
    C = self._execPath\
      + " -pflotranin "\
      + self._runFile
    return C

  def __repr__(self):
    return self._runFile + " -> jupypft.model.Model()"
  
  '''
  Getters & Setters
  aka methods that return the value of the attribute
  and modify their values
  '''
  @property
  def templateFile(self) -> str: return self._templateFile
  @templateFile.setter
  def templateFile(self,templateFile) -> None: self._templateFile = templateFile

  @property
  def runFile(self) -> str: return self._runFile
  @runFile.setter
  def runFile(self,runFile) -> None: self._runFile = runFile

  @property
  def execPath(self) -> str: return self._execPath
  @execPath.setter
  def execPath(self,execPath) -> None: self._execPath = execPath

  @property
  def folder(self) -> str: return self._folder
  @folder.setter
  def folder(self,folder) -> None: self._folder = folder

  @property
  def description(self) -> str: return self._description
  @description.setter
  def description(self,description) -> None: self._description = description
 
  '''
  Class variable «getters»
  aka methods that return the value of static attributes
  '''
  @classmethod
  def num_of_models(cls) -> float: return cls.__numberOf
    
  @classmethod
  def list_of_models(cls) -> list: return cls.__listObjs
  
  @classmethod
  def resetListOfModels(cls) -> None: cls.__listObjs = []
  
  '''
  Instance methods
  '''
  def cloneTemplate(self) -> None:
    '''
    Creates a copy of the template file as the
    this.runFile
    '''
    system("cp " + self.templateFile + " " + self.runFile)

    
  def replaceTagInFile(
    self,
    var
    ) -> None:
    '''
    Replace the variable tag for its value 
    in the PFLOTRAN input file (runFile)
    '''
    if var.value is None:
      print("Object has no value asigned :/ \n Try set_value() first")
    else:
      C = "sed -i 's/" + var.tag + "/"\
        + var.strValue\
        + "/g' " + self.runFile
      system(C)
  
  def runModel(self) -> None:
    '''
    Run PFLOTRAN executable with the input file 
    '''
    system(self._execPath \
      + " -pflotranin " \
#      + self._folder \
#      + "/" \
      + self.runFile + " " 
      + self._verboseAppend)

  def fixedToCSV(self,outputFile) -> None:
    '''
    Takes an output files from PFLOTRAN and convert them to a
    comma separated.
    '''
    system('''
      file={0}
      # Delete leading spaces
      sed -i 's/^  //g' $file
      sed -i '1s/^ //g' $file
      # Keep headers in other file
      head -1 $file > header.hidden
      # Delete header from file
      sed -i '1d' $file
      # Delete strings
      sed -i '1s/"//g' $file
      # Replace spaces for commas
      sed -i 's/  /,/g' $file
      sed -i 's/ /,/g' $file
      # Add the header again
      cat header.hidden $file > temp.file
      # Organize stuff
      mv temp.file $file
      rm header.hidden
      # Print end message
      echo "DONE with " $file
      '''.format(outputFile)
      )

  '''
  Class methods
  '''
  @classmethod
  def runAllModels(
    cls,
    nProcs=1,
    ) -> None:
    '''
    Run PFLOTRAN .in files on all the folders named
    with the given prefix. This function requires GNU Parallel
    instaled in the machine. 
    
    nProcs: int
      Number of cores to parallel run. Default 1
      
    NOTE: This is different than mpirun !!
    '''
    with open("taskForParallel.txt","w") as f:
      for ob in cls.__listObjs:
        f.write("{0} -pflotranin {1} \n"\
          .format(ob.execPath,ob.runFile))
             
    system('''
      parallel --jobs {0} < taskForParallel.txt
      '''.format(nProcs)
    )
  
  @classmethod
  def folderFixedToCSV(cls,folder) -> None:
    '''
    Takes a folder of output files from PFLOTRAN and convert them to a
    comma separated.
    '''
    system('''
      FOLDER={0}

      for file in $FOLDER/*
      do
        NCOMMAS=$(head -1 $file | grep -o '"' | wc -l)
        if [ $NCOMMAS -gt 0 ]
        then
          # Keep headers in other file
          head -1 $file > header.hidden
          # Delete leading spaces
          sed -i 's/^ //g' header.hidden
          # Delete strings
          sed -i 's/"//g' header.hidden

          # Delete header from file
          sed -i '1d' $file
          # Delete leading spaces
          sed -i 's/^  //g' $file
          # Replace spaces for commas
          sed -i 's/  /,/g' $file
          sed -i 's/ /,/g' $file

          # Add the header again
          cat header.hidden $file > temp.file
          
          # Organize stuff
          mv temp.file $file
          rm header.hidden
          
          # Print end message
          echo "DONE with " $file
        else
          echo "FILE PROPERLY WORKS"
        fi
      done
      '''.format(folder)
      )
  
        
'''
Functions
--------------
Non-dimensional numbers
'''
## Non-dimensional numbers
def DamkII(K,A,U,L,asString=False):
  '''Return the second Damköhler number'''
  DaII = ((L*L*K)/(A*U) if A>0 else float('inf'))
  return "{:.1E}".format(DaII) if asString else DaII

def Peclet(A,L,U,asString=False):
  '''Return the Peclet number'''
  Pe = (L*U)/(A*U) if A>0 else float('inf')
  return "{:.1E}".format(Pe) if asString else Pe

'''
Functions
--------------
Create a structured grid with unhomogeneous sizes
'''
def buildDXYZ(
  lenght,
  growRatio,
  numberOfElements,
  hasBump=False) -> str:
  '''
  lenght: float
    Lenght of the domain
  growRatio: float
    Ratio between the size of the last and the initial element
    d_N/d_0
      if R > 1, smallest is the initial element
      if R < 1, largest is the initial element
      if R == 1, all elements are the same
  numberOfElements: int 
    Size of the grid. Only handles even values(!)
  hasBump: bool
    Similar to transfinite GMSH withHump.
  '''
  
  import numpy as np
   
  # Avoid close to zero growRatios
  if abs(growRatio) < 1e-8: growRatio = 1
  numberOfElements = int(numberOfElements)
  
  if hasBump:
    N = math.floor(numberOfElements/2.0) 
    K = np.abs(growRatio)**(1/(N-1))
    listIntegers = list(range(N))
    KPow = [K**i for i in listIntegers]
    
    # Array of distances
    D = np.zeros(N)
    if numberOfElements%2 == 1:
      L = lenght/(2.0 + 1.0/np.sum(KPow))
    else:
      L = lenght/2.0
    
    #print("L",L)
    
    D[0] = L/(np.sum(KPow))
    for i in range(1,N):
      D[i] = D[0] * KPow[i]
    
    #print("D",D,np.sum(D))
    
    '''If the growRatio was negative, a short to long 
    grid was expected'''
    if growRatio < 0: D = np.flip(D)
    
    # Concatenate with an extra one in the middle
    if numberOfElements%2 == 1:
      D2 = np.concatenate((np.flip(D),[D[0]],D))
    else:
      D2 = np.concatenate((np.flip(D),D))
    
    #print("D2",D2,np.sum(D2))
    
    D3 = np.around(D2,decimals=2)
    partialSum = np.sum(D3)
    err = lenght - partialSum
    D3[0] += err/2
    D3[-1] += err/2
    
    #print("D3",D3,np.sum(D3))
  
  else:
    numberOfElements = int(numberOfElements)
  
    # Cell-to-cell ratio (K)
    K = np.abs(growRatio)**(1/(numberOfElements-1))
    listIntegers = list(range(numberOfElements))
    KPow = [K**i for i in listIntegers]

    # Array of distances
    D = np.zeros(numberOfElements)
    D[0] = lenght/(np.sum(KPow))
    for i in range(1,numberOfElements):
      D[i] = D[0] * KPow[i]

    # Array of rounded distances
    D2 = np.around(D,decimals=2)
    partialSum = np.sum(D2[:-1])
    D2[-1] = lenght - partialSum
  
    '''If the growRatio was negative, a short to long 
    grid was expected'''
    if growRatio < 0: D2 = np.flip(D2)
  
    D3 = D2
  
  '''Format as a long string'''
  F1 = ""
  for i in range(len(D3)):
    F1+="{:.4f} ".format(D3[i])
    if i == (len(D3)-1):
      F1+=" \\n    "
    elif i % 2 == 1 and i+1 < len(D3):
      F1+="\\\\ \\n    "

  return F1

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
# tagsReplaceable =  {
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
# tagsAccesory =  {
#   "FlowVel"   : "poreWaterVel",
#   "PoreVol"   : "poreVolume",
#   "pH"        : "pH",
#   "IonicStr"  : "IS"
# }

# ## Path to PFLOTRAN executable
# PFLOTRAN_path = "$PFLOTRAN_DIR/src/pflotran/pflotran "

# ## Table with the set of parameters
# try:
#   parameters_file = str(sys.argv[1])
# except IndexError:
#   sys.exit("Parameters file not defined :(")

# setParameters = read_csv(parameters_file)
# total_rows = setParameters.shape[0]

# ## Template for the PFLOTRAN input file
# try:
#   template_file = str(sys.argv[2])
# except IndexError:
#   sys.exit("Template file not found :(")

# ## Run cases?
# try:
#   shouldRunPFLOTRAN = "-run" in str(sys.argv[3])
# except IndexError:
#   shouldRunPFLOTRAN = False

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