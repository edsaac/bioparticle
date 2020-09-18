# VirusTransport_RxSandbox
PFLOTRAN Reaction Sandbox for virus transport

Trying to replicate results from this paper: 

Sadeghi, G., Schijven, J.F., Behrends, T., Hassanizadeh, S.M., Gerritse, J. and Kleingeld, P.J. (2011), Systematic Study of Effects of pH and Ionic Strength on Attachment of Phage PRD1. Groundwater, 49: 12-19. doi:10.1111/j.1745-6584.2010.00767.x

http://doi.wiley.com/10.1111/j.1745-6584.2010.00767.x

## Conceptual Model

![gifBioparticle](/images/virusBlob.gif)

**Mathematical description:**

![img](http://www.sciweavers.org/tex2img.php?eq=%5Cbegin%7Bequation%2A%7D%0A%5Cbegin%7Barray%7D%7Brr%7D%0A%20%20%20%20%5Cdfrac%7B%5Cpartial%20C%7D%7B%5Cpartial%20t%7D%20%2B%20%5Cdfrac%7B1%7D%7B%5Ctheta%7D%5C%3A%5Cvec%7Bq%7D%20%5Ccdot%20%5Cnabla%20C%20%20-%20%5Cnabla%20%5Ccdot%20%28D%5Cnabla%20C%29%20%3D%26%20-%20k_%7B%5Crm%20att%7DC%20%2B%20%5Cdfrac%7B1%7D%7B%5Ctheta%7Dk_%7B%5Crm%20det%7DS%20-%5Clambda_%7B%5Crm%20aq%7D%20C%5C%5C%0A%20%20%20%20%5C%5C%0A%20%20%20%20%5Cdfrac%7B1%7D%7B%5Ctheta%7D%5Cdfrac%7B%5Cpartial%20S%7D%7B%5Cpartial%20t%7D%20%3D%26%20k_%7B%5Crm%20att%7DC%20-%20%5Cdfrac%7B1%7D%7B%5Ctheta%7Dk_%7B%5Crm%20det%7DS%20-%5Clambda_%7B%5Crm%20im%7D%20S%5C%5C%0A%5Cend%7Barray%7D%0A%5Cend%7Bequation%2A%7D&bc=White&fc=Black&im=png&fs=18&ff=ccfonts,eulervm&edit=0)


## Instructions

```
cp src/reaction_sandbox_escPTr.F90  $PFLOTRAN_DIR/src/pflotran/reaction_sandbox_escPTr.F90
cp src/reaction_sandbox.F90  $PFLOTRAN_DIR/src/pflotran/reaction_sandbox.F90
python3 $PFLOTRAN_DIR/python/src/python/pflotran_depedencies.py
cd $PFLOTRAN_DIR/src/pflotran/
make pflotran
```

Details at https://bitbucket.org/pflotran/pflotran/wiki/Documentation/ReactionSandbox
