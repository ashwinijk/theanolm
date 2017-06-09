#!/bin/bash

# before running the script, create "lattices" folder in $THEANOLM_PATH folder and inside that create "slf" and "nbest" folder
# path to kaldi directories has to be set in path.sh file as we do in kaldi before running the script

. /nm-raid/audio/work/ajayakum/git/theanolm/recipes/penn-treebank/paths.sh

# Path to Kaldi and Theano folders
KALDI_PATH = "/nm-raid/audio/work/ajayakum/kaldi/egs/tedlium/s5"
THEANOLM_PATH = "/nm-raid/audio/work/ajayakum/git/theanolm/recipes/penn-treebank"


#######################  first convert kaldi lattice to text format  ################################
# Number of lattices

START=1
END=4

for (( c=$START; c<=$END; c++ ))
do
lattice-copy "ark:zcat $KALDI_PATH/exp/tri3/decode_test/lat.$c.gz |" ark,t:- | $KALDI_PATH/utils/int2sym.pl -f 3 $KALDI_PATH/data/lang_test/words.txt > $THEANOLM_PATH/lattices/lat.$c.txt || true
done

##############################   then convert that to slf format   ###################################

for (( c=$START; c<=$END; c++ ))
do
$KALDI_PATH/utils/convert_slf.pl $THEANOLM_PATH/lattices/lat.$c.txt $THEANOLM_PATH/lattices/slf || true
done
search_dir= $THEANOLM_PATH/lattices/slf
for entry in "$search_dir"/*
do
  echo "$entry" >> $THEANOLM_PATH/lattices/lattices.txt
done

####################  SLF lattices to N best list  ###################################################

lattice-tool -in-lattice-list $THEANOLM_PATH/lattices/lattices.txt -read-htk -nbest-decode 10 -out-nbest-dir $THEANOLM_PATH/lattices/nbest/ || true



