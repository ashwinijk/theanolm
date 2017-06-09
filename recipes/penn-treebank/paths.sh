# sample of the path settings

TRAIN_FILES=(/nm-raid/audio/work/ajayakum/git/theanolm/recipes/penn-treebank/simple-examples/data/ptb.train.txt)
DEVEL_FILE=/nm-raid/audio/work/ajayakum/git/theanolm/recipes/penn-treebank/simple-examples/data/ptb.valid.txt
EVAL_FILE=/nm-raid/audio/work/ajayakum/git/theanolm/recipes/penn-treebank/simple-examples/data/ptb.test.txt
OUTPUT_DIR=/nm-raid/audio/work/ajayakum/git/theanolm/recipes/penn-treebank
export PATH="$HOME/anaconda3/bin/:$PATH"
export PATH=/usr/local/cuda/bin:${PATH}
export THEANO_FLAGS='cuda.root=/usr/local/cuda/bin',device=cuda
export PYTHONPATH="$PYTHONPATH:$HOME/nm-raid/audio/work/ajayakum/git/theanolm/"
export PATH="$PATH:$HOME/nm-raid/audio/work/ajayakum/git/theanolm/bin"

## SRILM path setting (can be ignored if kaldi path is set since srilm is installed while installing kaldi) ####
export PATH="$PATH:$HOME/nm-raid/audio/work/ajayakum/git/theanolm/srilm/bin/i686-m64"

### kaldi path setting ####
export KALDI_ROOT=/nm-raid/audio/work/ajayakum/kaldi/
[ -f $KALDI_ROOT/tools/env.sh ] && . $KALDI_ROOT/tools/env.sh
export PATH=$PWD/utils/:$KALDI_ROOT/tools/openfst/bin:$PWD:$PATH:$KALDI_ROOT/tools/sph2pipe_v2.5
[ ! -f $KALDI_ROOT/tools/config/common_path.sh ] && echo >&2 "The standard file $KALDI_ROOT/tools/config/common_path.sh is not present -> Exit!" && exit 1
. $KALDI_ROOT/tools/config/common_path.sh
export LC_ALL=C

