FD_PATH=$(locate fast-downward.py | head -n 1)
${FD_PATH} $1 $2 --search "astar(lmcut())" | grep -e \([0-9]\) | awk '{$NF=""; print $0}'
