PFLOTRAN_path="$PFLOTRAN_DIR/src/pflotran/pflotran"
LIST=$(ls CASE*/*.in)
N=10

parallel --jobs $N $PFLOTRAN_path -pflotranin ::: $LIST

rm -rf PFTS || mkdir PFTS
cp CASE**/.pft PFTS/
cd ./miscellaneous
python3 organizeResults.py ../PFTS