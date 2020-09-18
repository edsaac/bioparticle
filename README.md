# VirusTransport_RxSandbox
PFLOTRAN Reaction Sandbox for virus transport

![gifBioparticle](/images/virusBlob.gif)


>Trying to replicate results from this paper: 
>
>Sadeghi, G., Schijven, J.F., Behrends, T., Hassanizadeh, S.M., Gerritse, J. and Kleingeld, P.J. (2011), Systematic Study of Effects of pH and Ionic Strength on >Attachment of Phage PRD1. Groundwater, 49: 12-19. doi:10.1111/j.1745-6584.2010.00767.x
>
>http://doi.wiley.com/10.1111/j.1745-6584.2010.00767.x


***

## Conceptual Model
![virusPaths](/images/virusPaths.png)
![boxModel](/images/boxModel.png)

**Mathematical description:**

![Eq.1](/images/Eqn1.png)


***

## Instructions

```
cp src/reaction_sandbox_escPTr.F90  $PFLOTRAN_DIR/src/pflotran/reaction_sandbox_escPTr.F90
cp src/reaction_sandbox.F90  $PFLOTRAN_DIR/src/pflotran/reaction_sandbox.F90
python3 $PFLOTRAN_DIR/python/src/python/pflotran_depedencies.py
cd $PFLOTRAN_DIR/src/pflotran/
make pflotran
```

Details at https://bitbucket.org/pflotran/pflotran/wiki/Documentation/ReactionSandbox
