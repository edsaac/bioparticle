## Compilation instructions

1. Add this new reaction sandbox (*BIOPARTICLE*) to PFLOTRAN's source folder.
```
cp src/reaction_sandbox_escPTr.F90  $PFLOTRAN_DIR/src/pflotran/reaction_sandbox_escPTr.F90
```
2. Replace the main reaction sandbox fortran file to include *BIOPARTICLE* as one of the options.
```
cp src/reaction_sandbox.F90  $PFLOTRAN_DIR/src/pflotran/reaction_sandbox.F90
```
3. Update dependencies.
```
python3 $PFLOTRAN_DIR/python/src/python/pflotran_depedencies.py
```
4. Compile PFLOTRAN code.
```
cd $PFLOTRAN_DIR/src/pflotran/
make pflotran
```

***

### ***Compilation details***

|Using|version|Link|
|--:|--:|--:|
|`PFLOTRAN`|`v3.0`|[![PFLOTRAN](https://img.shields.io/badge/&#x1f4a7;-PFLOTRAN-blue?style=flat)](https://www.pflotran.org/)|
|`PETSc`|`v3.13`|[![PETSc](https://img.shields.io/badge/&#129518;-PETSc-blue?style=flat)](https://www.mcs.anl.gov/petsc/)|
|`gfortran`|`7.5.0`|[![gfortran](https://img.shields.io/badge/-GNU%20Fortran-A42E2B?style=flat&logo=GNU)](https://gcc.gnu.org/fortran/)|
|`make`|`4.1`|[![make](https://img.shields.io/badge/-GNU%20Make-A42E2B?style=flat&logo=GNU)](https://www.gnu.org/software/make/)|
|`Ubuntu`|`v18.04`|[![ubuntu](https://img.shields.io/badge/-Ubuntu-black?style=flat&logo=ubuntu)](https://ubuntu.com/)|

***

**More details about compiling a new PFLOTRAN's reaction sandbox. >>** [&#128279;](https://bitbucket.org/pflotran/pflotran/wiki/Documentation/ReactionSandbox)

<a href="https://edsaac.github.io/bioparticle/">
	<img alt="Back" src="https://img.shields.io/badge/&#11013;-Go back-purple?style=for-the-badge">
</a>

<p align="right">
    <img src="https://img.shields.io/badge/Works on-my machine-purple?style=for-the-badge">
    <img src="https://img.shields.io/badge/-&#127802;-purple?style=for-the-badge">
</p>