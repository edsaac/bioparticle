<link rel="shortcut icon" type="image/x-icon" href="./images/favicon.png">

# Instructions

### Available reaction sandboxes

- BIOPARTICLE
  - Decay rates:
    - CONSTANT
    - TEMPERATURE_MODEL
  - Attachment rate:
    - CONSTANT
    - FILTRATION_MODEL
  - Detachment rate:
    - CONSTANT

## To Compile

1. Add this reaction sandbox to PFLOTRAN's source folder.
```
$ cp src/reactionSandbox/reaction_sandbox_*.F90 $PFLOTRAN_DIR/src/pflotran/
```
2. Replace the main reaction sandbox fortran file to include these sandboxes as one of the options.
```
$ cp src/reactionSandbox/reaction_sandbox.F90 $PFLOTRAN_DIR/src/pflotran/reaction_sandbox.F90
```
3. Add this reaction sandbox to the list of objects to compile
```
$ cp src/reactionSandbox/pflotran_object_files.txt $PFLOTRAN_DIR/src/pflotran/pflotran_object_files.txt
```
4. Update dependencies.
```
$ cd $PFLOTRAN_DIR/src/pflotran/
$ python3 ../python/pflotran_depedencies.py
```
5. Compile PFLOTRAN code.
```
$ cd $PFLOTRAN_DIR/src/pflotran/
$ make pflotran
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