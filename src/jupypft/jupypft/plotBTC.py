import numpy as np
import matplotlib.pyplot as plt

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
  
    plt.figure(figsize=(9,4),facecolor="white")
    
    ## Plot log-scale
    ax1 = plt.subplot(1,2,1)
    ax1.plot(X,Y,c="purple",lw=3)
    ax1.axvline(x=1.0,ls="dotted",c="gray",lw=1)
    ax1.axhline(y=1.0,ls="dashed",c="teal",lw=1)
    ax1.axhspan(ymin=-1.0E-7,ymax=1.0E-6,facecolor="pink",alpha=0.2)
    
    ax1.set_yscale("symlog",\
      linthresh=1.0E-6,subs=[1,2,3,4,5,6,7,8,9])
    ax1.set_ylim([-1.0E-7,1.15])

    ax1.set_xlabel("Time [$-$]",fontsize="large")
    ax1.set_ylabel("C/C₀ [$-$]",fontsize="large")
            
    ## Plot linear-scale
    ax2 = plt.subplot(1,2,2)
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
    
if __name__ == "__main__":
    main()
