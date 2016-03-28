#!/usr/bin/python2.7 

import logging
from plumbum import cli
from plumbum import local
from plumbum.cmd import gawk, sort, mawk, parallel
from plumbum.cmd import grep, wc, cat, head
import sys
import re
import os
import time

class Dist(cli.Application):
    _hosts=''
    _block = ''
    _delim = '[^a-zA-Z0-9]+'
    _params = ['-Mx', '--pipe', '--fifo', '--bg' ]
    _jobs = "-j+0"
    _files = 'cat'

    #_rmt_cmd = "mawk -vRS='%s' '{a[tolower($1)]+=1} END { for(k in a) { print a[k],k} }'".strip() % (_delim)
    #time /usr/bin/parallel 
    
    
    "/usr/bin/numactl -l  /usr/bin/mawk -vRS='[^a-zA-Z0-9]+' '{a[tolower(\$1)]+=1} END { for(k in a) { print a[k],k} }'"
    _endcmd = mawk["/bin/mawk '{a[$2]+=$1} END {for(k in a) {if (a[k] > 1000) print a[k],k}}' | sort -nr | head -10"]

    _rmt_cmd = "/usr/bin/numactl -l  /usr/bin/mawk -vRS='[^a-zA-Z0-9]+' '{a[tolower(\$1)]+=1} END { for(k in a) { print a[k],k} }'"
    _reorg_cmd = "{a[$2]+=$1} END {for(k in a) {if (a[k] > 100) print a[k],k}}"

    @cli.switch("-z", str, help="Filenames. Named pipes are your friend here.")
    def filenames(self, filenames):
        for file in filenames.split():
            if os.path.isfile(file):
                file_str = '<%s' % file
                self._files += file_str

            else:
                print "One or more files don't exist."
        print self._files

    @cli.switch("-d", str, help="Delimiter for wc. Default: %s" % _delim)
    def delim(self, delim):
        """Delim for wc'ing. Currently: %s""" % _delim
        try:
            re.compile(delim)
        except:
            print "Bad regex. Try again."
            sys.exit(1)

        self._delim = delim

    @cli.switch("-b", str, help="Block size. 128M works great on my laptop/server.")
    def block(self, block):
        block_re = re.compile('^[0-9]+[KMGTPkmgtp]{,1}$')
        
        if not block_re.match(block):
            print "Bad block specification!"
            sys.exit(1)

        else:
            self._block = ['--block', block ]

    @cli.switch("-S", str, help="Host list in 'thread#/hostname' format, eg; '24/servername'")
    def hostnames(self, hostnames):
        hostnames = hostnames.split(',')
        tmp_hostnames = []

        tmp = [ host.split('/') for host in hostnames ]
        for hostdef in tmp:
            if len(hostdef) == 1:
                tmp_hostnames.append(''.join(hostdef))

            elif len(hostdef) == 2 and hostdef[0].isdigit():
                tmp_hostnames.append('/'.join(hostdef))
            else:
                print "Bad hosts definition. Format is '#cores/hostname'"
                exit(1)

        self._hosts = '-S' + ','.join(tmp_hostnames)

    def main(self, *srcfiles):
        [ self._params.append(param) for param in 
                [  self._hosts,  self._rmt_cmd,  self._files, self._jobs ] 
                 ]

        cat('/home/matt/Business_Licenses.csv') | parallel(self._params) | mawk(self._reorg_cmd)
        print test
        print test()

if __name__ == "__main__":
    Dist.run()
