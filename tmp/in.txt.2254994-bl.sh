#!/bin/sh
#PBS -v PATH
#$ -v PATH


para=$1
cd /home/ol/data/xushijie/PKAD2_rev
./tmp/in.txt.2254994-bl.pl 0 $para &
./tmp/in.txt.2254994-bl.pl 1 $para &
./tmp/in.txt.2254994-bl.pl 2 $para &
./tmp/in.txt.2254994-bl.pl 3 $para &
./tmp/in.txt.2254994-bl.pl 4 $para &
./tmp/in.txt.2254994-bl.pl 5 $para &
./tmp/in.txt.2254994-bl.pl 6 $para &
./tmp/in.txt.2254994-bl.pl 7 $para &
wait

