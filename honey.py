#!/usr/bin/env python

import os
import sys
import threading
import time
import socket


class honey(threading.Thread):
    """Honeypot, nice, simple, extendable"""
    def __init__(self, host='', port=6000, pl=[]):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.plugins = pl
        self.running = True

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        while self.running:
            (insock, address) = s.accept()
            data = None
            try:
                data = insock.recv(1024)
            except socket.error:
                pass
            insock.close()
            for p in self.plugins:
                try:
                    p.main(address[0], address[1], self.host, self.port, data)
                except:
                    pass


def getPlugins(path=os.getcwd() + '/pl/'):
    ret = []
    if not os.path.exists(path):
        os.makedirs(path)
    if path not in sys.path:
        sys.path.insert(0, path)
    for p in os.listdir(path):
        if p.endswith(".py"):
            p = p[:-2]
            ret.append(__import__(p))
    return ret

if __name__ == '__main__':
    host = ''
    ports = [3000]
    threads = []
    plugins = getPlugins()
    print "[+] Loaded %s" % str([a.__name__ for a in plugins])
    try:
        for port in ports:
            print '[+] Starting port %s:%d thread...' % (host, port)
            threads.append(honey(host, port, plugins))
            threads[-1].daemon = True
            threads[-1].start()
    except BaseException, e:
        print '[-] Error: %s' % (e)
        exit(1)
    # Run forever, or until we kill it >.>
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print '[+] Exiting...'
        for thread in threads:
            thread.running = False
        time.sleep(1)
        exit(0)
