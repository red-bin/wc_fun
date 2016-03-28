#!/bin/bash


COMMANDFILE=$1
MAXTHREADS=$2

running_thread_count=0
running_treads=""

echo $running_thread_count $MAXTHREADS

IFS="
"
for line in `cat $COMMANDFILE` ; do
  while [ $running_thread_count -ge $MAXTHREADS ] ; do
    #echo $running_thread_count
    for arr_cnt in `seq 0 $MAXTHREADS` ; do
      if [ ! -d /proc/${running_threads[$arr_cnt]} ] ; then
        echo "${running_threads[$arr_cnt]} is done. Continuing on.."
        unset running_threads[$arr_cnt]
        running_thread_count=$((running_thread_count-1))
      fi
    sleep .5
    done
  done

  bash -cl "$line" & #Run command of the show
  last_thread=$!
  echo "Running bash -cl \"$line\" as PID $last_thread"

  for arr_cnt in `seq 0 $MAXTHREADS` ; do 
    if [ "${running_threads[$arr_cnt]}" = "" ] ; then
      running_threads[$arr_cnt]=$last_thread
      running_thread_count=$(($running_thread_count+1))
      break
    fi
  done
done 
echo "Thread spreader done, the following threads remain: ${running_threads}"
wait 
