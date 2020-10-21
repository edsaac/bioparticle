#############################################
#
# convert .msh file into ugi for PFLOTRAN
#
#############################################

fileName=$1
endFile="column.ugi"
rm $endFile

whNodesIni=$(awk '/Nodes/{ print NR; exit}' $fileName)
whNodesEnd=$(awk '/EndNodes/{ print NR; exit}' $fileName)

sed -n "${whNodesIni},${whNodesEnd}p" $fileName > aux1
sed -i '$d' aux1
sed -i '1,2d' aux1

cut -d " " -f 2,3,4 aux1 > nodesAux
rm aux1
numNode=$(wc -l nodesAux | cut -d " " -f 1)

whElemIni=$(awk '/Elements/{ print NR; exit}' $fileName)
whElemEnd=$(awk '/EndElements/{ print NR; exit}' $fileName)

sed -n "${whElemIni},${whElemEnd}p" $fileName > aux1
sed -i '$d' aux1
sed -i '1,2d' aux1

# Find 3D 8-node HEX
awk '$2 == "5" { print $0 }' aux1 | cut -d " " -f 6-13 > elemAux
sed -i 's/^/H /' elemAux

# Find 2D 4-node HEX
## Bottom Face
name="bottom"
awk '$2 == "3" { print $0 }' aux1 | awk '$4 == "2" { print $0 }' | cut -d " " -f 6-9 > $name.ss
sed -i 's/^/Q /' $name.ss
numBound=$(wc -l ${name}.ss | cut -d " " -f 1)
sed -i "1 s/^/${numBound}\n/" $name.ss

## Top Face
name="top"
awk '$2 == "3" { print $0 }' aux1 | awk '$4 == "3" { print $0 }' | cut -d " " -f 6-9 > $name.ss
sed -i 's/^/Q /' $name.ss
numBound=$(wc -l ${name}.ss | cut -d " " -f 1)
sed -i "1 s/^/${numBound}\n/" $name.ss

## Sides Face
name="sides"
awk '$2 == "3" { print $0 }' aux1 | awk '$4 == "4" { print $0 }' | cut -d " " -f 6-9 > $name.ss
sed -i 's/^/Q /' $name.ss
numBound=$(wc -l ${name}.ss | cut -d " " -f 1)
sed -i "1 s/^/${numBound}\n/" $name.ss

rm aux1
numElem=$(wc -l elemAux | cut -d " " -f 1)

echo "$numElem $numNode" > $endFile
cat elemAux nodesAux >> $endFile

rm elemAux nodesAux
