FOLDER=$1

for file in $FOLDER
do
  NCOMMAS=$(head -1 $file | grep -o '"' | wc -l)
  if [ $NCOMMAS -gt 0 ]
  then
    sed -i 's/^  //g' $file
    sed -i '1s/^ //g' $file
    sed -i '1s/"//g' $file
    sed -i 's/  /,/g' $file
    echo "FIXED FILE"
  else
    echo "NOTHING DONE"
  fi
done