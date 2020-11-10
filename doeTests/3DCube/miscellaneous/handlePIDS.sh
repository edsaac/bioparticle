PFLOTRAN_path="$PFLOTRAN_DIR/src/pflotran/pflotran"
LIST=$(ls CASE*/*.in)
N=10

parallel --jobs $N $PFLOTRAN_path -pflotranin ::: $LIST