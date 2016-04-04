#!/bin/bash -e

totNum=$(find ../ -name "*.pdb" -maxdepth 1 | wc -l)
i=0

for f in $(find ../ -name "*.pdb" -maxdepth 1)
do 
  prefix=$(echo $f | awk -NF "[/]+" '{print $2}')
  genPairStat -s $f -n ../processMain/shadowMap.log -o $prefix.log -f $f \
2>/dev/null > /dev/null
  
  i=$((i+1))
  printf '\r'$i"/%d is finished." $totNum
done

printf '\n'
echo "*************************"
echo process.res EXITS NORMALLY
echo "*************************"
