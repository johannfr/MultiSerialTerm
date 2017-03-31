#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import threading
import time
import sys
import os

class SerialThread(threading.Thread):
    def __init__(self, serial_queue):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.baudrate = 115200
        self.portname = None
        self.serial_port = serial.Serial(timeout=1)
        self.serial_port.baudrate = self.baudrate
        self.serial_queue = serial_queue

    def run(self):
        while True:
            if self.serial_port.isOpen():
                sys.stdout.flush()
                line = self.serial_port.readline()
                if line:
                    self.serial_queue.put("%s\n"%line.strip())

                continue

            time.sleep(0.1)

    def set_port(self, portname):
        if self.serial_port.isOpen():
            self.serial_port.close()
        if os.name == "posix":
            self.portname = "/dev/%s"%portname
        else:
            self.portname = portname
        self.serial_port.setPort(self.portname)
        self.serial_port.open()


    def set_baudrate(self, baudrate):
        if self.serial_port.isOpen():
            self.serial_port.close()

        baudrate = int(baudrate.split()[0])
        self.baudrate = baudrate
        self.serial_port.baudrate = baudrate
        if self.portname is not None:
            self.serial_port.open()

    def close(self):
        self.serial_port.close()
