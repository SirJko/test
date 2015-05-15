#!/bin/bash -e

counter=$2
counter2=1
file="$1".txt
echo "This is the start of line generator" > "$file"

while [ $counter -gt 0 ] ; do
	echo "Line #$counter2" >> "$file"
	counter=$[$counter-1];
	counter2=$[$counter2+1];
done
