#!/bin/sh
#   #   # #   #   #   #       #   #             #   #                       #
extras="-Mx"
hosts="-S:"
jobnum="-j+0"
mawkcmd='mawk'
blocksize="--block 3.5M"

optcnt=0
while getopts ":S:j:b:s:m:" o ; do
    case "${o}" in
        S) hosts="-S${OPTARG}" ; optcnt=$(($optcnt+1)) ;;
        j) jobnum="-j${OPTARG}" ; optcnt=$(($optcnt+1)) ;;
        b) blocksize="--block ${OPTARG}" ; optcnt=$(($optcnt+1)) ;;
        m) max="${OPTARG}" ; optcnt=$(($optcnt+1)) ;;
        *) echo ":(" && exit 1 ;;
    esac
done
for i in `seq 1 $optcnt` ; do shift ; done

function post_process() {
    /usr/bin/$mawkcmd '{words[$2]+=$1} END \
            {for(w in words) { if (words[w] > 1000) print words[w],w}}' \
        | sort -S0 -nr \
        | head -${1}
}

RMTFUNC="/usr/bin/numactl -l \
    $mawkcmd -vRS='[^a-zA-Z0-9]+'
        '{ words[tolower(\$1)] += 1 } END \
         { for(w in words) { print words[w],w} }'"

params=" $extras $jobnum $hosts --pipe --fifo $blocksize"

for i in `seq 1 ${#}` ; do 
    cat $1 
    shift
done | parallel $params $RMTFUNC | post_process $max
