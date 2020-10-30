PFLOTRAN_path="$PFLOTRAN_DIR/src/pflotran/pflotran"
LIST=$(ls CASE*/*.in)
N=10

task(){
  local run=$1
}

for d in $LIST ; do
   ((i=i%N)); ((i++==0)) && wait
   task "$PFLOTRAN_path -pflotranin $d" &
done

