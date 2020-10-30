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
