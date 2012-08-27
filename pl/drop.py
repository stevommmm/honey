#!/usr/bin/env python

import subprocess


def main(ex_host, ex_port, self_host, self_port, data):
    if ex_host == '127.0.0.1':
        return
    drop = subprocess.Popen(["iptables", "-A", "INPUT", "-s", ex_host, "-j", "DROP"],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, error = drop.communicate()
    if out:
        print out
    else:
        print error
