#! /bin/sh
project_loca="$(dirname "$(pwd)")"
dcf_pos=$project_loca"/code"
all_rmid=$project_loca"/result/light_curve"
cd $all_rmid

for file in ./*
do
		rmid=$file
		echo "$rmid"
		cd $rmid
		cp $project_loca"/code/dcf_f90" .
		input_argument="2\ndcf\nn\n0\nn\n100\ncont.txt\nHbetab.txt\n"
		printf "$input_argument" | ./dcf_f90
		cd $all_rmid
done
