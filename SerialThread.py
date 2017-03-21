#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import threading
import time
import sys

class SerialThread(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.serial_port = serial.Serial(timeout=1)
        self.callback = callback

    def run(self):
        while True:
            if self.serial_port.isOpen():
                sys.stdout.write("closed\n")
                sys.stdout.flush()

                time.sleep(0.2)
                continue

            self.callback("open")
            time.sleep(1)
