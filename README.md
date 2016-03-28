Mock wc using parallel along with pipes for threading
Using stdin/out seems to act as a decent throttle in
preventing cpu/netork bottlenecks.

Advantages:
Natural bottleneck limiting
Relatively modular
parallel is annoying to use. Less parallel = good
Minus mawk, uses standard linux packages.

Disadvantages
Ssh is slooow.
cmdline parameters shouldn't be moved around.
It took a lot of tweaking to get this to work between my server and laptop. Hopefully these settings should work for most scenarios, though.
ssh keys can be a pain


[matt@chaptop rackspace]$ time ./wordcount.sh -m4 -S192.168.82.140 ~/A50462_TcktsIssdSince2009.txt 
16163337 il
14960071 pas
11675100 paid
9298388 pm

real    3m51.285s
user    2m2.660s
sys     0m35.650s
[matt@chaptop rackspace]$ time ./wordcount.sh -m4 -S:,192.168.82.140 ~/A50462_TcktsIssdSince2009.txt 
16163337 il
14960071 pas
11675100 paid
9298388 pm

real    1m47.393s
user    3m45.997s
sys     0m32.080s
[matt@chaptop rackspace]$ time ./wordcount.sh -m4 -S: ~/A50462_TcktsIssdSince2009.txt 
16163337 il
14960071 pas
11675100 paid
9298388 pm

real    2m2.515s
user    4m56.003s
sys     0m29.477s

[matt@chaptop rackspace]$ time ./wordcount.sh -m4 -S:,32/192.168.82.140 ~/A50462_TcktsIssdSince2009.txt 
parallel: Warning: ssh to 192.168.82.140 only allows for 28 simultaneous logins.
parallel: Warning: You may raise this by changing /etc/ssh/sshd_config:MaxStartups and MaxSessions on 192.168.82.140.
parallel: Warning: Using only 27 connections to avoid race conditions.
16163337 il
14960071 pas
11675100 paid
9298388 pm

real    1m42.327s
user    3m36.887s
sys     0m29.950s
