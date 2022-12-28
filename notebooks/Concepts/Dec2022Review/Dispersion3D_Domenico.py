import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from math import floor, log10
from os import system

import matplotlib.colors as colors
import matplotlib.ticker as ticker
plt.style.use(f'/home/edsaa/Repositories/ReactiveBiomass/misc/edwin.mplstyle')

''' GLOBAL CONSTANTS '''
PI = np.pi
BOLTZMANN = 1.380649E-23 #N·m/K
TEMP = 10 + 273.15 #K
g = 9.81 #m/s²

def sci_notation(num, decimal_digits=1, precision=None, exponent=None):
    """
    Returns a string representation of the scientific
    notation of the given number formatted for use with
    LaTeX or Mathtext, with specified number of significant
    decimal digits and precision (number of decimal digits
    to show). The exponent to be used can also be specified
    explicitly.
    """
    if exponent is None:
        exponent = int(floor(log10(abs(num))))
    coeff = round(num / float(10**exponent), decimal_digits)
    if precision is None:
        precision = decimal_digits

    return r"${0:.{2}f}\times10^{{{1:d}}}$".format(coeff, exponent, precision)

def p_notation(num) -> str:
    exponent = np.log10(num)
    return rf"$10^{{{exponent:.0f}}}$"

def dispCoef(D_m,alpha_L,U,n=1.0):
    return D_m + alpha_L*(U**n)

def poreVel(q, theta):
    return q/theta

def molecularDiff(visco,dp): 
    return (BOLTZMANN*TEMP)/(3*PI*visco*dp)

def attachmentRate(dc,theta,alpha,U,eta0): 
    return (3*(1-theta)*alpha*U*eta0)/(2*dc)

def collectorEff(etaD,etaI,etaG):
    return etaD + etaI + etaG

def collectorEfficiency_Diffusion(A_s,N_R,N_Pe,N_vdW):
    return 2.40 * (A_s**(1./3.)) * (N_R**-0.081) * (N_Pe**-0.715) * (N_vdW**0.052)

def collectorEfficiency_Interception(A_s,N_R,N_Pe,N_vdW):
    return 0.55 * A_s * (N_R**1.55) * (N_Pe**-0.125) * (N_vdW**0.125)

def collectorEfficiency_GDeposition(N_gr,N_R,N_Pe,N_vdW):
    return 0.475 * (N_gr**1.11)   * (N_R**-1.35)  * (N_Pe**-1.11)  * (N_vdW**0.053)

def happelParameter(theta):
    s = 1-theta
    s53 = s**(5./3.)
    s13 = s**(1./3.)
    s21 = s**2
    return (2*(1-s53))/(2 - (3*s13) + (3*s53) - (2*s21))

def noDim_SizeRatio(dp,dc):
    return dp/dc

def noDim_Péclet(q,dc,Dm):
     return q*dc/Dm

def noDim_vanderWaals(A):
    return A/(BOLTZMANN*TEMP)

def noDim_Gravitational(dp,rhof,rhop):
    return (PI*(dp**4)*(rhop-rhof)*g)/(12.*BOLTZMANN*TEMP)

'''CASE CONSTANTS'''
#Porosity
theta = 0.35 # adim
dc = 2.0E-3 # 2mm << sand
dp = 1.0E-7
A = 5.0E-21 # J = N·m
viscosity = 0.0008891 # N·s/m²
water_density = 999.79 # kg/m³
particle_density = 1050.0 # kg/m³ 
alpha = 0.01 # adim << favorable conditions

#Darcy flow velocity
#I = 1e-3
H = 10.
r = 40.
f = 10.
Qin = 0.24/86400.
decayRate = 3.5353E-06

def hydraulicCond_kozenycarman(dc:np.array) -> np.array:
    kappa = dc**2 * np.power(theta,3)/ (180 * np.power(1-theta, 2))
    return kappa * water_density * g / viscosity

K = hydraulicCond_kozenycarman(dc)

def characteristic_q(I:np.array) -> np.array:
    return K*I + Qin*(1+f)/(4*r*H)

def transversal_dispersivity(q:np.array, dc:np.array, dp: float):
    Dm = molecularDiff(viscosity,dp)
    αKt, mKt = 0.025, 1.10 
    KtDm_ratio = 0.70 + αKt*np.power(dc * q/theta / Dm, mKt)
    return KtDm_ratio * Dm

def longitudinal_dispersivity(q:np.array, dc:np.array, dp: float):
    Dm = molecularDiff(viscosity,dp)
    αKl, mKl = 0.50, 1.20 
    KlDm_ratio = 0.70 + αKl*np.power(dc * q/theta / Dm, mKl)
    return KlDm_ratio * Dm

def katt_dp_dc(dp:np.array, dc:np.array, q:np.array):

    #Molecular diffusion
    Dm  = molecularDiff(viscosity,dp)
    
    #Pore water velocity
    U   = poreVel(q,theta)
    
    #Non-dimensional numbers
    As  = happelParameter(theta)
    NR  = noDim_SizeRatio(dp,dc)
    NPe = noDim_Péclet(q,dc,Dm)
    NvW = noDim_vanderWaals(A)
    NGr = noDim_Gravitational(dp,water_density,particle_density)
    
    #Collector efficiency
    etaD = collectorEfficiency_Diffusion(As,NR,NPe,NvW)
    etaI = collectorEfficiency_Interception(As,NR,NPe,NvW)
    etaG = collectorEfficiency_GDeposition(NGr,NR,NPe,NvW)
    eta0 = collectorEff(etaD,etaI,etaG)
    
    #Attachment rate
    kAtt = attachmentRate(dc,theta,alpha,U,eta0)

    return kAtt

from scipy.special import erfc
from scipy.special import erf

Y,Z = 0.40, 0.50

def dispersion_advection(xx,yy,zz,Kl,Kt):
    V = q/theta
    Cnot = 1.0/(q*Y*Z)
    alphaL = Kl/V
    alphaT = Kt/V
    decaySolver = decayRate + katt
    determinant = 1 - np.sqrt(1.0 + (4*decaySolver*alphaL/V))
    exponential = np.exp(xx/(2*alphaL)*determinant)
    denominator = 2 * np.sqrt(xx * alphaT)
    omega = (erf((yy + Y/2)/denominator) - erf((yy - Y/2)/denominator)) * (erf((zz + Z/2)/denominator) - erf((zz - Z/2)/denominator))
    return Cnot * exponential * omega * Qin


#############################
## Plotting 
#############################

x = np.linspace(0.01,99,201)
y = np.linspace(-1.49,1.49,101)
xx,yy = np.meshgrid(x,y)
z = st.slider("Z(m)", min_value=0.0, max_value=5.0, value=0.25)

Iarray = [1e-3,1e-2,1e-1]
fig,axs = plt.subplots(2, len(Iarray), sharex=True, sharey="row", figsize=(12,6),
    gridspec_kw={"hspace":0.1, "wspace":0.05})

contour_kw = dict(colors=["springgreen"], alpha=0.8, linewidths=2.5)
contour_label_kw = dict(inline=True, fmt="%.0f", fontsize=12, colors=["springgreen"])
pcolormesh_kw = dict(vmin=0, vmax=0.1, cmap='bone_r', edgecolors='face')

for I, ax in zip(Iarray, axs[0]):

    #I = st.number_input("Gradient", min_value=1e-10, max_value=1e2, value=1e-3, format="%.2E")
    q = characteristic_q(I)
    Kl = longitudinal_dispersivity(q,dc,dp)
    Kt = transversal_dispersivity(q,dc,dp)
    katt = katt_dp_dc(dp,dc,q)
    Ce = dispersion_advection(xx, yy, z, Kl, Kt)
    logCe = -np.ma.log10(np.ma.masked_less(Ce, 1e-20))
    
    img = ax.pcolormesh(xx, yy, Ce,**pcolormesh_kw)

    cs = ax.contour(xx, yy, logCe, [4],**contour_kw)
    ax.clabel(cs, cs.levels, **contour_label_kw)
    #ax.set_title(f"$I=${sci_notation(I)}\n")
    ax.text(
        10, 1.0, f"$I = ${p_notation(I)} m/m\n$q = ${sci_notation(q)} m/s", rotation=0, size=9,
        zorder=10, ha='left', va='center',
        bbox=dict(boxstyle="rarrow,pad=0.3", fc="#6495ed55", ec="cornflowerblue", lw=0.5))

####################
x = np.linspace(0.01,99,201)
y = st.slider("Y(m)", min_value=0.0, max_value=5.0, value=0.0)
z = np.linspace(-1.0,1.9,101)
xx,zz = np.meshgrid(x,z)

for I, ax in zip(Iarray,axs[1]):
    ## Calculations
    q = characteristic_q(I)
    Kl = longitudinal_dispersivity(q,dc,dp)
    Kt = transversal_dispersivity(q,dc,dp)
    katt = katt_dp_dc(dp,dc,q)
    Ce = dispersion_advection(xx, y, zz, Kl, Kt)
    logCe = -np.ma.log10(np.ma.masked_less(Ce, 1e-20))

    img = ax.pcolormesh(xx, -zz, Ce, **pcolormesh_kw)
    cs = ax.contour(xx, -zz, logCe, [4], **contour_kw)
    ax.clabel(cs, cs.levels, **contour_label_kw)

    ax.annotate(f'Concentration\n$C_0 = ${Ce.max():.2f}', 
        xy=(0,0), xytext=(40.0, -1.0), xycoords='data', 
        fontsize=10, ha='center', va='center',
        bbox=dict(boxstyle='square', fc='blue',alpha=0.20),
        arrowprops=dict(arrowstyle="->",
                shrinkA=0, shrinkB=2, ec="cornflowerblue",
                connectionstyle="angle,angleA=-10,angleB=120,rad=10"))

plt.colorbar(img,ax=axs.flatten(),
        orientation='horizontal', location='top',
        anchor=(0.5,-0.2),
        label="Concentration " + r"$C = \frac{M}{qYZ}$" + "\n",
        shrink=0.3)

fig.supxlabel("Distance from contamination   $x$ [m]")
axs[0,0].set_ylabel("Horizontal distance   $y$ [m]", fontsize=8)
axs[1,0].set_ylabel("Depth   $z$ [m]", fontsize=8)
for ax in axs.flatten(): ax.spines.right.set_visible(False)
st.pyplot(fig)


###############

# x = np.linspace(0.01,50,100)
# y = np.linspace(-1.5,1.5,51)
# z = np.linspace(0.0,4.0,51)

# xx,yy,zz = np.meshgrid(x,y,z)

# import pyvista as pv
# from stpyvista import stpyvista

# ## Set up plotter
# plotter = pv.Plotter(window_size=[600,600])
# surface = pv.StructuredGrid(xx, yy, zz)
# surface.point_data["Ce"] = (zz).flatten()
# #dispersion_advection(xx, np.ones_like(Ce), zz, Kl, Kt).flatten().T
# # surface.add_field_array(dispersion_advection(surface.x, surface.y, surface.z, Kl, Kt), "Ce")
# st.code(surface)
# plotter.add_mesh(surface, scalars="Ce", show_edges=False)
# plotter.view_xy()
# ## Pass the plotter (not the mesh) to stpyvista
# stpyvista(plotter)

# def dispersion_advection(xx,yy,zz,Kl,Kt,time):
#     V = q/theta
#     Y,Z = 0.50, 0.50
#     decaySolver = decayRate + katt
#     beta = np.sqrt(np.power(V,2)/(4 * np.power(Kl,2)) + decaySolver/Kl)
#     determinant = np.sqrt(V + (4*decaySolver*Kl))
#     gammaPlus  = (xx + determinant*time)/(2 * np.sqrt(Kl*time))
#     gammaMinus = (xx - determinant*time)/(2 * np.sqrt(Kl*time))
#     Fsolver = 0.5 * (\
#         (np.exp(-beta*xx + (V*xx/(2*Kl))) * erfc(gammaMinus)) \
#         + \
#         (np.exp(beta*xx + (V*xx/(2*Kl)) * erfc(gammaPlus))))
#     denominator = 2 * np.sqrt(xx * Kt/V)
#     omega = 0.25 * (erf((yy + Y/2)/denominator) - erf((yy - Y/2)/denominator)) * (erf((zz + Z/2)/denominator) - erf((zz - Z/2)/denominator))
#     return Fsolver * omega