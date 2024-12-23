#!/usr/bin/bash

counter=1
n=10

if [[ $# -gt 0 ]]; then
    n=$1
fi

pattern1='^>([^_]+)_(hg38)_.*'
pattern2='^>([^_]+)_([^_]+)_.*'
while IFS= read -r line; do
    if [[ $line =~ $pattern1 ]]; then
	nl=">${BASH_REMATCH[2]}"
	block=$nl
    else    
	if [[ ! "$line" =~ ^[[:space:]]*$ ]]
	then
	    if [[ $line =~ $pattern2 ]]; then
		nl=">${BASH_REMATCH[2]}"
		block=$block"\n"$nl
	    else
		block=$block"\n"$line
	    fi
	else
	    if [[ $block =~ ">" ]]
	    then
		echo -e $block > "output$counter.fa"
		iqtree2 -s output$counter.fa  --redo
		block=""
		counter=$(($counter+1))
		if [[ $counter -gt 100 ]]
		then
		   break
		fi
	    fi
	fi
    fi
done



