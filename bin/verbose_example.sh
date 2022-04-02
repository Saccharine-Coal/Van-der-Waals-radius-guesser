echo "Working dir=$PWD"
DIR="$( cd "$( dirname "$0" )" && cd .. && pwd )"
python3 $DIR/src/limits_from_xyz.py $DIR/docs/example/Te.mol

python3 $DIR/src/limits_from_xyz.py $DIR/docs/example/Te.xyz
