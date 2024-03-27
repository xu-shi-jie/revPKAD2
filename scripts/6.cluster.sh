# !/bin/bash

# Author: Shijie Xu
# Date: 2023-07-07
# Description: This script is used to create a cluster.

# read all fasta files in the folder and concatenate them into one file with '\n' as the separator for each file
in_path="tmp/in.txt"
db30="tmp/db30.txt"

# cd-hit with 90% identity, coverage 0.3
# cd-hit -i $in_path -o $db90 -c 0.9 -n 5 -g 1 -d 0 -p 1 -T 16 -M 0
# cd-hit with 60% identity, coverage 0.3
# cd-hit -i $db90 -o $db60 -c 0.6 -n 4 -g 1 -d 0 -p 1 -T 16 -M 0
# psi-cd-hit with 25% identity, coverage 0.3
# https://github.com/weizhongli/cdhit/blob/master/psi-cd-hit/README.psi-cd-hit
./cdhit/psi-cd-hit/psi-cd-hit.pl -i $in_path -o $db30 -c 0.3 -ce 1e-6 -G 0 -g 1 -para 8 -blp 4