#!/usr/bin/env python
import time


def main(ex_host, ex_port, self_host, self_port, data):
    f = open('loghoney.txt', 'a', 0)
    separator = '=' * 40
    f.write('Time: %s\nServer Port: %d\nIP Address: %s\nPort: %d\nData: %s\n%s\n\n' %
            (time.ctime(), self_port, ex_host, ex_port, data, separator))
    f.close()
