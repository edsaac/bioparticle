import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import argmin
from pandas import read_csv
import os

## New functions 
import jupypft.model as mo
import jupypft.parameter as pm

def xyPlotLine(
        inputFile = "./pflotran-obs-0.tec",
        XIndex=0,
        YIndex=3,
        normalizeXWith=1.0,
        normalizeYWith=1.0,
        legend = ""
               ):
    '''
    inputFile : str 
        PFLOTRAN .tec output file
    XIndex : int
        Column index that holds the time for the plot
    YIndex : int
        Column that holds the variable for the plot
    normalizeXWith : float
        Value to normalize variable in x axis
    normalizeYWith : float
        Value to normalize variable in y axis

    '''
    
    DATA = np.loadtxt(inputFile,delimiter=",",skiprows=1)
    X = DATA[:,XIndex]/normalizeXWith
    Y = DATA[:,YIndex]/normalizeYWith
  
    plt.figure(figsize=(5,8),facecolor="white")
    
    ## Plot log-scale
    ax1 = plt.subplot(2,1,1)
    ax1.plot(X,Y,c="purple",lw=3)
    ax1.axvline(x=1.0,ls="dotted",c="gray",lw=1)
    ax1.axhline(y=1.0,ls="dashed",c="teal",lw=1)
    ax1.axhspan(ymin=-1.0E-7,ymax=1.0E-6,facecolor="pink",alpha=0.2)
    
    ax1.set_yscale("symlog",\
      linthresh=1.0E-6,subs=[1,2,3,4,5,6,7,8,9])
    ax1.set_ylim([-1.0E-7,1.15])

    plt.setp(ax1.get_xticklabels(), visible=False)
    ax1.set_ylabel("C/C₀ [$-$]",fontsize="large")
            
    ## Plot linear-scale
    ax2 = plt.subplot(2,1,2, sharex=ax1)
    ax2.plot(X,Y,c="purple",lw=3)
    ax2.axhline(y=1.0,ls="dashed",c="teal",lw=1)
    ax2.axvline(x=1.0,ls="dotted",c="gray",lw=1)
    
    ax2.set_ylim([-1.0E-2,1.02])
    
    ax2.set_xlabel("Time [$-$]",fontsize="large")
    ax2.set_ylabel("C/C₀ [$-$]",fontsize="large")
    ax2.text(0.8,0.9,"max(C)/C₀ = {:.2f}%".format(max(Y*100)),\
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.25),\
        horizontalalignment='right',transform=ax2.transAxes)
          
    plt.tight_layout()  
    plt.show()

def plotMassBalancesInFolder(
        folderToPlot,
        indices = {'t':0,'q':26,'m':28},
        normalizeWith={'t':1.0,'q':1.0,'m':1.0},
        legendTitle = ""
               ):
    '''
    folderToPlot : str 
        Path to folder where all the files to be plotted are found
    indices : dict
        Column index for the time 't', water mass rate 'q' and 
        mass extraction rate 'm'.
        e.g.: {'t':str,'q':str,'m':str}
    normalizeWith : dict
        Value to normalize variable in y axis
        e.g.: {'t':float,'q':float,'m':float}
    legendTitle : str
        It receives TeX notation.
    '''
    listOfFiles = os.listdir(folderToPlot)
    listOfFiles.sort()
    
    def get_cmap(n, name='Set1'): ## Color map for plots 
      return plt.cm.get_cmap(name, n)
    
    cmap = get_cmap(max(len(listOfFiles),9))
    
    plt.figure(figsize=(7,5))
    ax1 = plt.subplot(1,1,1)
    
    for i,f in enumerate(listOfFiles):
      DATA = read_csv(\
        folderToPlot+"/"+f,\
        delimiter=",")
    
      t = DATA[indices['t']]/normalizeWith['t']
      q = DATA[indices['q']]/normalizeWith['q']
      m = DATA[indices['m']]/normalizeWith['m']
      
      X = t
      Y = np.divide(m,q)
      
      logRed = -np.log10(max(Y))
      labelText = r"$\bf{" + f[:-8].replace("_","\ ") + r"}$" \
                  + "\n  ·" + r'$-log[max(C)/C₀] =$ ' + "{:.1f}".format(logRed)
        
      ax1.plot(X,Y,c=cmap(i),lw=2.5,label=labelText)
    
    ## Plot log-scale
    ax1.axhline(y=1.0,ls="dashed",c="teal",lw=1)
    ax1.axhspan(ymin=-1.0E-7,ymax=1.0E-6,facecolor="pink",alpha=0.2)
    
    ax1.set_yscale("symlog",\
      linthresh=1.0E-6,subs=[1,2,3,4,5,6,7,8,9])
    ax1.set_ylim([-1.0E-7,1.15])

    ax1.set_ylabel("C/C₀ [$-$]",fontsize="large")       
    ax1.set_xlabel("Time [$d$]",fontsize="large")
    
    ncol = (1,1) [len(listOfFiles) > 3]
    l = ax1.legend(title=legendTitle,ncol=ncol,\
      bbox_to_anchor=(1,0), loc="lower left")
    
    plt.setp(l.get_title(), multialignment='center')
    
    plt.tight_layout()  
    plt.show()

def plotEndConcentrations(
        folderToPlot,
        Xdata,
        indices = {'t':0,'q':26,'m':28},
        normalizeWith={'t':1.0,'q':1.0,'m':1.0},
        legendTitle = ""
               ):
    '''
    folderToPlot : str 
        Path to folder where all the files to be plotted are found
    indices : dict
        Column index for the time 't', water mass rate 'q' and 
        mass extraction rate 'm'.
        e.g.: {'t':str,'q':str,'m':str}
    normalizeWith : dict
        Value to normalize variable in y axis
        e.g.: {'t':float,'q':float,'m':float}
    legendTitle : str
        It receives TeX notation.
    '''
    listOfFiles = os.listdir(folderToPlot)
    listOfFiles.sort()
    
    def get_cmap(n, name='Set1'): ## Color map for plots 
      return plt.cm.get_cmap(name, n)
    
    cmap = get_cmap(max(len(listOfFiles),9))
    
    plt.figure(figsize=(6,8))
    ax1 = plt.subplot(1,1,1)
    
    logC_arr = np.zeros_like(Xdata)
    
    for i,f in enumerate(listOfFiles):
      DATA = read_csv(\
        folderToPlot+"/"+f,\
        delimiter=",")
    
      q = DATA[indices['q']]/normalizeWith['q']
      m = DATA[indices['m']]/normalizeWith['m']
      
      Y = np.divide(m,q)
      maxY = np.max(Y)
      logC_val = -np.log10(maxY)
      logC_arr[i] = logC_val
      
    print(logC_arr)  
    
    ax1.plot(Xdata,logC_arr,c=cmap(0),lw=3,marker='o')
    
    ## Plot log-scale
    whereWorst = np.argmin(logC_arr - np.min(logC_arr))
    worstC = np.min(logC_arr)
    worstI = Xdata[whereWorst]
    ax1.axhline(y=worstC,ls="dashed",c="teal",lw=1,\
      label="log-reduction: {:.1f}".format(worstC))
    
    ax1.axvline(x=worstI,ls="dashed",c="teal",lw=1,\
      label=r"$\bf{I} = $" + " {:.2E}".format(worstI))
   
    ax1.set(ylim=[0,10],xlim=[1.0E-4,1.0E-1])
    ax1.set_xscale("log")
    ax1.set_ylabel(r"$\bf{-log(C/C_0)}$ [-]",fontsize="large")       
    ax1.set_xlabel(r"$\bf{I}$ [m/m]",fontsize="large")
    
    ncol = (1,1) [len(listOfFiles) > 3]
    l = ax1.legend(title=legendTitle,ncol=ncol,loc="lower left")
    
    plt.setp(l.get_title(), multialignment='center')
    
    plt.tight_layout()  
    plt.show()

if __name__ == "__main__":
    main()
