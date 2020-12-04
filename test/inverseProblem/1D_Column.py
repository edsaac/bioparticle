#!/usr/bin/env python
# coding: utf-8

# # This is a notebook that runs PFLOTRAN in the background
# # for the breakthrough curve of a columns experiment

# In[1]:


get_ipython().run_line_magic('reset', '-f')
import numpy as np
import matplotlib.pyplot as plt

from ipywidgets import interact_manual
import ipywidgets as wd

from os import system

## New functions 
import PFLOTRAN as PFLO


# In[2]:


L = 50 #cm
ConcentrationAtInlet = 1.66E-16 #mol/L
InjectTimeInPoreVol = 1.25


# In[3]:


ColumnModel = PFLO.Model()
TemplateFile = "./template.in"


# Parameters with a fixed value:

# In[4]:


Porosity     = PFLO.Var(tag="<porosity>",value=0.37,units="adim")
FlowVelocity = PFLO.Var(tag="<darcyVel>",value=0.7585,units="cm/h")


# Parameters with a fixed value but calculated from other parameters

# In[5]:


ElutionTime  = PFLO.Var(tag="<elutionTime>",                        value=L/(FlowVelocity.get_value()/Porosity.get_value())*InjectTimeInPoreVol*3600,                        units="s")

EndTime      = PFLO.Var(tag="<endTime>",                        value=10.*InjectTimeInPoreVol,                        units="d")


# Parameters whose values are set by a widget:

# In[6]:


LongDisp     = PFLO.Var(tag="<longDisp>",units="cm")
RateAttachment = PFLO.Var(tag="<katt>",units="1/h")
RateDetachment = PFLO.Var(tag="<kdet>",units="1/h")
RateDecayAqueo = PFLO.Var(tag="<decayAq>",units="1/h")
RateDecayImmob = PFLO.Var(tag="<decayIm>",units="1/h")


# In[7]:


listOfParameters = [
    Porosity,
    LongDisp,
    FlowVelocity,
    ElutionTime,
    EndTime,
    RateAttachment,
    RateDetachment,
    RateDecayAqueo,
    RateDecayImmob
]


# In[8]:


def plotResults(FILE = "./pflotran-obs-0.tec"):

    textBoxDimensionless =       "Péclet = $\\dfrac{\\rm advection}{\\rm dispersion} = $" +       PFLO.Peclet(LongDisp.get_value(),L,FlowVelocity.get_value(),asString=True)
    
    ObservationPoint = np.loadtxt(FILE,delimiter=",",skiprows=1)
    Cnorm = ObservationPoint[:,3]/ConcentrationAtInlet
    TimeInPoreVolumes = ObservationPoint[:,0] * (FlowVelocity.get_value()*24.)/L
  
    Legend=["$\\dfrac{[V_{(aq)}]}{[V_{(aq)}]_0}$"]
    plt.figure(figsize=(12,8),facecolor="white")
    
    ## Plot log-scale
    ax1 = plt.subplot(2,2,1)
    ax1.plot(TimeInPoreVolumes,Cnorm,c="purple",lw=3)
    ax1.set_yscale("symlog",      linthresh=1.0E-6,subs=[1,2,3,4,5,6,7,8,9])
    ax1.set_ylim([-1.0E-7,1.15])
    ax1.set_xlim([0,6])
    ax1.set_xlabel("Pore Volume [$-$]",fontsize="large")
    ax1.axvline(x=InjectTimeInPoreVol,ls="dotted",c="gray",lw=1)
    ax1.axhspan(ymin=-1.0E-7,ymax=1.0E-6,facecolor="pink",alpha=0.2)

        
    ## Péclet number
    ax1.text(5.5,5.0E-3,textBoxDimensionless,        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.25),        horizontalalignment='right')
    
    ## Plot linear-scale
    ax2 = plt.subplot(2,2,2)
    ax2.plot(TimeInPoreVolumes,Cnorm,c="purple",lw=3,label=Legend[0])
    ax2.set_ylim([-1.0E-2,1.02])
    ax2.set_xlim([0,6])
    ax2.set_xlabel("Pore Volume [$-$]",fontsize="large")
    ax2.axvline(x=InjectTimeInPoreVol,ls="dotted",c="gray",lw=1)
    ax2.legend(fontsize="large",loc="upper right")
  
    ## Damköhler II numbers
    Damkohler = [PFLO.DamkII(RateAttachment.get_value(),                            LongDisp.get_value(),                            FlowVelocity.get_value(),                            L,asString=False),
                PFLO.DamkII(RateDetachment.get_value(),\
                            LongDisp.get_value(),\
                            FlowVelocity.get_value(),\
                            L,asString=False),
                PFLO.DamkII(RateDecayAqueo.get_value(),\
                            LongDisp.get_value(),\
                            FlowVelocity.get_value(),\
                            L,asString=False),
                PFLO.DamkII(RateDecayImmob.get_value(),\
                            LongDisp.get_value(),\
                            FlowVelocity.get_value(),\
                            L,asString=False)]
    tickLabels = ["$k_{\\rm att}$","$k_{\\rm det}$","λ$_{\\rm aq}$","λ$_{\\rm im}$"]
    
    ax3 = plt.subplot(2,2,3)
    ax3.bar(x=range(len(Damkohler)), height=Damkohler, tick_label=tickLabels, log=True, hatch="/")
    ax3.set_ylabel("Damköhler(II) = $\\dfrac{\\rm reaction}{\\rm dispersion}$",fontsize='large')
    
    ## Parameters of the reaction sandbox
    parametersTable = [["$k_{\\rm att}$",RateAttachment.get_strValue(),"h$^{-1}$"],                       ["$k_{\\rm det}$",RateDetachment.get_strValue(),"h$^{-1}$"],                       ["$\lambda_{\\rm aq}$",RateDecayAqueo.get_strValue(),"h$^{-1}$"],                       ["$\lambda_{\\rm im}$",RateDecayImmob.get_strValue(),"h$^{-1}$"],                       ["α$_{\\rm L}$",LongDisp.get_strValue(),"cm"]]
    
    ax4 = plt.subplot(2,2,4)
    table = ax4.table(cellText=parametersTable,              colLabels=["Parameter","Value","Unit"],              loc='center',colWidths=[0.3,0.3,0.3],edges="horizontal")
    table.set_fontsize(34)
    table.scale(1,2.5)
    ax4.axis('off')
    
    plt.tight_layout()  
    plt.show()


# In[9]:


def RunAll(logLongDisp,logKAtt,logKDet,logDecayAq,logDecayIm):
    ColumnModel.cloneTemplate(TemplateFile)
    
    RateAttachment.set_value(logKAtt)
    RateDetachment.set_value(logKDet)
    RateDecayAqueo.set_value(logDecayAq)
    RateDecayImmob.set_value(logDecayIm)
    LongDisp.set_value(logLongDisp)
       
    for parameter in listOfParameters:
        parameter.replaceTag()
    ColumnModel.runModel()
    ColumnModel.fixTecFile()
    plotResults()


# In[10]:


RateAttachment.set_slider(    wd.FloatLogSlider(value=0.0400,base=10, min=-10, max=1, step=0.1,                      description=r'\(k_{\text{att}}\) [1/h]',                       style={'description_width': 'initial'}))

RateDetachment.set_slider(    wd.FloatLogSlider(value=0.0026,base=10, min=-10, max=1, step=0.1,                      description=r'\(k_{\text{de}}\) [1/h]',                       style={'description_width': 'initial'}))

RateDecayAqueo.set_slider(    wd.FloatLogSlider(value=0.0070,base=10, min=-10, max=1, step=0.1,                      description=r'\(\lambda_{\text{aq}}\) [1/h]',                       style={'description_width': 'initial'}))

RateDecayImmob.set_slider(    wd.FloatLogSlider(value=0.0350,base=10, min=-10, max=1, step=0.1,                      description=r'\(\lambda_{\text{im}}\) [1/h]',                       style={'description_width': 'initial'}))

LongDisp.set_slider(    wd.FloatLogSlider(value=0.2,base=10, min=-10, max=2, step=0.1,                      description=r'\(\alpha_{L}\) [1/h]',                       style={'description_width': 'initial'}))


# In[11]:


interact_manual(RunAll,    logLongDisp = LongDisp.get_slider(),    logKAtt = RateAttachment.get_slider(),    logKDet = RateDetachment.get_slider(),    logDecayAq = RateDecayAqueo.get_slider(),    logDecayIm = RateDecayImmob.get_slider()    );
              


# **Péclet = Advection Rate/Dispersion Rate**
# 
# \begin{equation}
#     \text{P}_{é} = \dfrac{LU}{D}
# \end{equation}

# **Damköhler(II) = Reaction Rate/Dispersion Rate**
# 
# \begin{equation}
#     \text{D}_{A,II} = \dfrac{L^2k}{D}
# \end{equation}

#       "Damköhler(II) = $\\dfrac{\\rm reaction}{\\rm dispersion}$"+"\n" +\
#       "Da$^{\\rm kat} = $"+ PFLO.DamkII(RateAttachment.get_value(),\
#                                      LongDisp.get_value(),\
#                                      FlowVelocity.get_value(),\
#                                      L,asString=True) +"\n" +\
#       "Da$^{\\rm kde} = $"+ PFLO.DamkII(RateDetachment.get_value(),\
#                                      LongDisp.get_value(),\
#                                      FlowVelocity.get_value(),\
#                                      L,asString=True) +"\n" +\
#       "Da$^{\\rm λaq} = $"+ PFLO.DamkII(RateDecayAqueo.get_value(),\
#                                      LongDisp.get_value(),\
#                                      FlowVelocity.get_value(),\
#                                      L,asString=True) +"\n" +\
#       "Da$^{\\rm λim} = $"+ PFLO.DamkII(RateDecayImmob.get_value(),\
#                                      LongDisp.get_value(),\
#                                      FlowVelocity.get_value(),\
#                                      L,asString=True) +"\n" +\
#                                      
#     
#     ## Rate values
#     ax1.text(5.5,5.0E-4,textBoxKin,\
#         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),\
#         horizontalalignment='right')                           
#                                      
#     textBoxKin = \
#       "$k_{\\rm att} = $" + RateAttachment.get_strValue() + " h$^{-1}$" +"\n" + \
#       "$k_{\\rm det} = $"+ RateDetachment.get_strValue() + " h$^{-1}$" +"\n" + \
#       "$\lambda_{\\rm aq} = $ "+ RateDecayAqueo.get_strValue() + " h$^{-1}$" +"\n" + \
#       "$\lambda_{\\rm im} = $ "+ RateDecayImmob.get_strValue() + " h$^{-1}$" +"\n" + \
#       "α$_{\\rm L} = $ " + LongDisp.get_strValue() + " cm "

# In[ ]:




