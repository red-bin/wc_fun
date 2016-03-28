Essentially a non-alphanumeric wc that uses parallel with ssh for more power. The local host is used to send data over ssh and de-serialize the data that comes back.  This gives pretty good performance, since it limits bottlenecks.

This is done in a way that everything is kept in transit and is only stored in memory as long as it needs to be.  It seems to take very, very little memory to parse fairly large files.

The command line is a little bit finicky. I'll fix up the readme soon and add a help doc. For now, the bottom examples might work fine.

##Requirements:
    numactl -- on remote machines
    mawk -- on all machines (or change the script for awk/gawk)
    parallel -- on master machine

##Advantages:
    Natural bottleneck limiting
    Takes multiple files
    Relatively modular
    Less interaction with parallel!
    mawk is very, very fast.

##Disadvantages

    Ssh is slooow. Create an ssh config for just this to use a different cypher if security doesn't matter. 
    Settings might need work. These were the best for my laptop which hosted the file.
    ssh keys.
    The requirements are a little annoying, but they should be in most distros' repos.

###Test file
```
$ ls -lrth A50462_TcktsIssdSince2009.txt 
-rw-r--r-- 1 matt matt 2.1G Mar 15 02:36 A50462_TcktsIssdSince2009.txt
```

###My normal way without (much) parallelism:
```
$ time tr '[:upper:]' '[:lower:]' < ~/A50462_TcktsIssdSince2009.txt | sed -r 's/[^A-Za-z0-9]+/\n/g'  | grep . | sort --parallel=2 | uniq -c | sort -nr --parallel=2 | head -4                                                        
16163337 il
14960071 pas
11675100 paid
  9298388 pm
real    8m20.731s
user    8m59.020s
sys     0m10.683s
```

### Single remote host:
```
$ time ./wordcount.sh -m4 -S111.111.111.111 ~/A50462_TcktsIssdSince2009.txt 
16163337 il
14960071 pas
11675100 paid
9298388 pm
real    3m51.285s
user    2m2.660s
sys     0m35.650s
```

### Remote host and local host:
```
$ time ./wordcount.sh -m4 -S:,192.168.82.140 ~/A50462_TcktsIssdSince2009.txt 
16163337 il
14960071 pas
11675100 paid
9298388 pm
real    1m47.393s
user    3m45.997s
sys     0m32.080s
```

### Just local host:
```
$ time ./wordcount.sh -m4 -S: ~/A50462_TcktsIssdSince2009.txt 
16163337 il
14960071 pas
11675100 paid
9298388 pm
real    2m2.515s
user    4m56.003s
sys     0m29.477s
```

###Adding more cores speeds it up.... slightly:
```
$ time ./wordcount.sh -m4 -S:,32/111.111.111.111 ~/A50462_TcktsIssdSince2009.txt 
16163337 il
14960071 pas
11675100 paid
9298388 pm
real    1m42.327s
user    3m36.887s
sys     0m29.950s
```
