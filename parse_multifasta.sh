#!/usr/bin/bash

counter=1
while IFS= read -r line; do
    if [[ $line == ">"*hg38* ]]
    then
	echo $line
	block=$line
    else    
	if [[ ! "$line" =~ ^[[:space:]]*$ ]]
	then
	    block=$block"\n"$line
	    
	else
	    if [[ $block =~ ">" ]]
	       
	    then
		echo -e $block > "output$counter.fa"
		iqtree2 -s output$counter.fa  --redo
		block=""
		counter=$(($counter+1))
		if [[ $counter -gt 10 ]]
		then
		   break
		fi
	    fi
	fi
    fi
done



