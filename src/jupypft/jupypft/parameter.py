#!/usr/bin/python3

'''
Module for keeping the parameters and variables
encountered in PFLOTRAN cases
'''  

from os import system
import ipywidgets as wd
from ipywidgets.widgets.widget_string import Label

class Parameter:
  '''
  Class for parameters to set in a PFLOTRAN case
  '''
  __numberOf = 0   # Counter of all instantiated variables 
  __listObjs = []    # List of all instantiated variables 
  __listTags = []    # List of all tags
  
  def __init__(
    self,
    tag,
    value=None,
    mathRep=""
    ):
    '''
    Parameters
    ---------------
    tag: str
      The tag to replace in the template file
    value: float, optional
      The value of the parameter
    mathRep : str, optional
      The Latex representation of the parameter, e,g, $k_{att}$
    '''
    self._tag = tag
    self._value = value
    self._mathRep = mathRep

    Parameter.__numberOf += 1
    Parameter.__listTags.append(tag)
    Parameter.__listObjs.append(self)
  
  def __str__(self):
    if self.mathRep == "":
      return self.tag + " = " + self.strValue
    else:
      return self.mathRep + " = " + self.strValue
  
  def __repr__(self):
    return self.tag + " = " + self.strValue
  
    # return "jupypft.parameter.Parameter(\"" \
    #   + self.tag + "\")"

  # def __setattr__(self, key, value):
  #   raise TypeError( "%r won't accept new attributes" % self )
  '''
  Getters & Setters
  aka methods that return the value of the attribute
  and modify their values
  '''
  @property
  def tag(self) -> str: return self._tag
  @tag.setter
  def tag(self,tag) -> None: self._tag = tag
  
  @property
  def value(self) -> float: return self._value
  @value.setter
  def value(self,value) -> None: self._value = value
  
  @property
  def mathRep(self) -> float: return self._mathRep
  @mathRep.setter
  def mathRep(self,mathRep) -> None: self._mathRep = mathRep
    
  @property
  def strValue(self) -> str: 
    try: return str(self._value)
    except TypeError: return str("<None>")
  
  '''
  Class variable «getters»
  aka methods that return the value of static attributes
  '''
  @classmethod
  def num_of_vars(cls) -> float: return cls.__numberOf
  
  @classmethod
  def list_of_tags(cls) -> list: return cls.__listTags
  
  @classmethod
  def list_of_vars(cls) -> list: return cls.__listObjs
  
  @classmethod
  def rebuildListOfObjects(cls,d,clean=True):
    if clean: cls.__listObjs = []
    for _, v in d.items():
      if isinstance(v, dict):
        cls.rebuildListOfObjects(v,clean=False)
      else:
        cls.__listObjs.append(v)

####################

class Real(Parameter):
  '''
  Class for real-valued parameters to set in a PFLOTRAN case
  
    e.g.
      permeability = var(tag="<K>",units="cm2")
  '''
  def __init__(
    self,
    tag,
    value=None,
    units="",
    mathRep="",
    ):
    '''
    Parameters
    ---------------
    tag: string
      The tag to replace in the template file
    value: float
      The value of the parameter
    units: string
      the units of the parameter - does nothing
    mathRep : str, optional
      The Latex representation of the parameter, e,g, $k_{att}$
    '''
    super().__init__(tag,value,mathRep=mathRep)
    self._units = units 

  '''
  Getters & Setters
  aka methods that return the value of the attribute
  and modify their values
  '''
  @property
  def units(self) -> str: return self._units
  @units.setter
  def units(self,units) -> None: self._units = units
  
  '''Polymorphic method!'''
  @property
  def strValue(self) -> str:
    try: return "{:.3E}".format(self._value)
    except TypeError: return str("<None>")
  
######

class Integer(Parameter):
  '''
  Class for integer-valued parameters to set in a PFLOTRAN case
  
    e.g.
      numberOfCells = Integer(tag="<nX>",units="-")
  '''
  def __init__(
    self,
    tag,
    value=None,
    units="",
    mathRep="",
    ):
    '''
    Parameters
    ---------------
    tag: string
      The tag to replace in the template file
    value: float
      The value of the parameter
    units: string
      the units of the parameter - does nothing
    mathRep : str, optional
      The Latex representation of the parameter, e,g, $k_{att}$
    )
    '''
    super().__init__(tag,value,mathRep=mathRep)
    self.units = units 

  '''
  Getters & Setters
  aka methods that return the value of the attribute
  and modify their values
  '''
  @property
  def units(self) -> str: return self._units
  @units.setter
  def units(self,units) -> None: self._units = units
  
  '''Polymorphic method!'''
  @property
  def strValue(self) -> str:
    try:  return "{:}".format(int(self._value))
    except TypeError: return str("<None>")
  
##############################

class JustText(Parameter):
  '''
  Class for text parameters to set in a PFLOTRAN case
  
    e.g.
      DXYZ = JustText(tag="<DX>")
  '''
  
  def __init__(
    self,
    tag,
    value=None,
    mathRep="",
    ):
    '''
    Parameters
    ---------------
    tag: string
      The tag to replace in the template file
    value: float
      The value of the parameter
    units: string
      the units of the parameter - does nothing
    mathRep : str, optional
      The Latex representation of the parameter, e,g, $k_{att}$
    )
    '''
    super().__init__(tag,value,mathRep=mathRep)
    
  '''
  Getters & Setters
  aka methods that return the value of the attribute
  and modify their values
  '''
  @property
  def strValue(self) -> str: 
    try: return self._value
    except TypeError: return str("<None>")


###################
class WithSlider(Real):
  '''
  Class for parameters to set in a PFLOTRAN case
  with a ipywidget slider to modify their value.

    e.g.
      permeability = var(tag="<K>",units="cm2",slider=FloatLogSlider())

  '''  
  def __init__(
    self,
    tag,
    value=None,
    units="",
    slider=wd.FloatLogSlider(),
    mathRep="",
    ):
    '''
    Parameters
    ---------------
    tag: string
      The tag to replace in the template file
    value: float
      The value of the parameter
    units: string
      the units of the parameter - does nothing
    slider: ipywidgets.FloatSlider()
      a widget to modify this.value
    mathRep : str, optional
      The Latex representation of the parameter, e,g, $k_{att}$
    '''
    self._slider = slider
    super().__init__(tag,self.slider.value,units,mathRep=mathRep)
    # self._floatBox = wd.FloatText()
    # self._link  wd.link((self._slider,'value'),(self._floatBox,'value'))
    self.buildui()
  '''
  Getters & Setters
  aka methods that return the value of the attribute
  and modify their values
  '''
 
  @property
  def value(self) -> float: 
    self._value = self.slider.value
    return self._value
  @value.setter
  def value(self,n) -> None: 
    self.slider.value = n
    self._value = n
    self.buildui()
 
  @property
  def slider(self) -> str: return self._slider
  @slider.setter
  def slider(self,wdslider) -> None: 
    self._slider = wdslider
    self.buildui()
  
  @property
  def ui(self) -> str: return self._ui
  def buildui(self) -> None: 
    # self._link = \
    #   wd.link((self._slider, 'value'), (self._floatBox, 'value'))
    self._ui = wd.HBox([
      wd.HTMLMath(value=self._mathRep),
#      self._floatBox,
      self._slider,
      wd.Label(value="["+ self._units + "]")])
  
  @property
  def strValue(self) -> str:
    if "Int" in str(self.slider):      
      try:  return "{:}".format(int(self._value))
      except TypeError: return str("<None>")    
    else:
      try: return "{:.3E}".format(self._value)
      except TypeError: return str("<None>")


###############################

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