PFLOTRAN_path="$PFLOTRAN_DIR/src/pflotran/pflotran"
LIST=$(ls CASE*/*.in)
N=10

for d in $LIST ; do
   ((i=i%N)); ((i++==0)) && wait
   echo "$PFLOTRAN_path -pflotranin $d"
   $PFLOTRAN_path -pflotranin $d &
done

