<link rel="shortcut icon" type="image/x-icon" href="./images/favicon.png">

# Instructions

### Available options in the reaction sandbox

- BIOPARTICLE
  - Decay rates:
    - CONSTANT
    - TEMPERATURE_MODEL
  - Attachment rate:
    - CONSTANT
    - FILTRATION_MODEL
  - Detachment rate:
    - CONSTANT

## **How to compile?**

Currently, the BIOPARTICLE sandbox is located on [a fork](https://bitbucket.org/edsaac/pflotran/src/bioparticle/) of the PFLOTRAN project. 

To use it, you can follow steps 1-3 in the [installation instructions](https://documentation.pflotran.org/user_guide/how_to/installation/linux.html#linux-install). For the fourth step, you will need to clone [this fork](https://bitbucket.org/edsaac/pflotran/src/bioparticle/), checkout the ```bioparticle``` branch and compile:

```
$ git clone https://edsaac@bitbucket.org/edsaac/pflotran.git 
$ cd $PFLOTRAN_DIR
$ git checkout bioparticle
$ mkdir bin
$ cd bin
$ make -j 8 -f ../src/pflotran/makefile SRC_DIR=../src/pflotran pflotran
```

## **How to use?**

### *BIOPARTICLE*

If all rates are set as CONSTANTS, the `CHEMISTRY` card should look something like this:

```
CHEMISTRY
  PRIMARY_SPECIES
    Vaq
  /
  
  IMMOBILE_SPECIES
    Vim
  /

  REACTION_SANDBOX
    BIOPARTICLE
      PARTICLE_NAME_AQ Vaq
      PARTICLE_NAME_IM Vim
      RATE_ATTACHMENT CONSTANT
        VALUE <katt> 1/h
      /
      RATE_DETACHMENT CONSTANT
        VALUE <kdet> 1/h
      /
      DECAY_AQUEOUS CONSTANT
        VALUE <decayAq> 1/h
      /
      DECAY_ADSORBED CONSTANT
        VALUE <decayIm> 1/h
      /
    /
  /
  LOG_FORMULATION
  TRUNCATE_CONCENTRATION 1.0E-35
  DATABASE rxn_database.dat
  OUTPUT
    TOTAL
    ALL
  /
END
```
If using temperature-based models for decay rates and colloid filtration theory for the attachment rate, the `CHEMISTRY` card should look something like this:

```
CHEMISTRY
  PRIMARY_SPECIES
    Vaq
  /
  
  IMMOBILE_SPECIES
    Vim
  /

  REACTION_SANDBOX
    BIOPARTICLE
      PARTICLE_NAME_AQ Vaq
      PARTICLE_NAME_IM Vim
      RATE_ATTACHMENT FILTRATION_MODEL
        DIAMETER_COLLECTOR <diamCollector>
        DIAMETER_PARTICLE <diamParticle>
        HAMAKER_CONSTANT <hamakerConstant>
        DENSITY_PARTICLE <rhoParticle>
      /
      RATE_DETACHMENT CONSTANT
        VALUE <kdet> 1/s
      /
      DECAY_AQUEOUS TEMPERATURE_MODEL
        TREF    4.0
        ZT      29.1
        N       2.0
        LOGDREF 2.3
      /
      DECAY_ADSORBED TEMPERATURE_MODEL
        TREF    4.0
        ZT      29.1
        N       2.0
        LOGDREF 2.3
      /
    /
  /
  LOG_FORMULATION
  TRUNCATE_CONCENTRATION 1.0E-50
  DATABASE ../MISCELLANEOUS/rxn_database.dat
  OUTPUT
    TOTAL
    ALL
  /
END
```
_____
## Installing the python API*

1. Add the package to your python installation using `pip`.
```
$ cd ./src/jupypft/
$ pip install -e .
```

***

### It worked when...

|Using|version|Link|
|--:|--:|--:|
|`PFLOTRAN`|`v3.0`|[![PFLOTRAN](https://img.shields.io/badge/&#x1f4a7;-PFLOTRAN-blue?style=flat)](https://www.pflotran.org/)|
|`PETSc`|`v3.13`|[![PETSc](https://img.shields.io/badge/&#129518;-PETSc-blue?style=flat)](https://www.mcs.anl.gov/petsc/)|
|`gfortran`|`7.5.0`|[![gfortran](https://img.shields.io/badge/-GNU%20Fortran-A42E2B?style=flat&logo=GNU)](https://gcc.gnu.org/fortran/)|
|`make`|`4.1`|[![make](https://img.shields.io/badge/-GNU%20Make-A42E2B?style=flat&logo=GNU)](https://www.gnu.org/software/make/)|
|`Ubuntu`|`v20.04`|[![ubuntu](https://img.shields.io/badge/-Ubuntu-black?style=flat&logo=ubuntu)](https://ubuntu.com/)|

***

**More details about compiling a new PFLOTRAN's reaction sandbox. >>** [&#128279;](https://bitbucket.org/pflotran/pflotran/wiki/Documentation/ReactionSandbox)

<a href="https://edsaac.github.io/bioparticle/">
	<img alt="Back" src="https://img.shields.io/badge/&#11013;-Go back-purple?style=for-the-badge">
</a>

<p align="right">
    <img src="https://img.shields.io/badge/Works on-my machine-purple?style=for-the-badge">
    <img src="https://img.shields.io/badge/-&#127802;-purple?style=for-the-badge">
</p>