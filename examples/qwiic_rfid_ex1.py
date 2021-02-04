# !/usr/bin/env python
# ----------------------------------------------------------------
# qwiic_rfid_ex1.py
#
# Basic example that reads tag and prints ID and the time requested
# when prompted by user.
# ----------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, January 2021
#
# This python library supports the SparkFun Electronics qwiic 
# sensor/board ecosystem on a Raspberry Pi (and compatible) single
# board computers.
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SParkFun. Buy a board!
# https://www.sparkfun.com/products/15191
# 
# ================================================================
# Copyright (c) 2021 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 1
#
# This example gets the latest tag scanned and it's associated time from the
# Qwiic RFID Reader when the user enters "1" into the terminal. The
# "scan" time is not the time of the day the RFID card was scanned but rather the
# time between when the card was scanned and when you the user requested the RFID
# tag from the Qwiic RFID Reader.

from __future__ import print_function
import qwiic_rfid
import time
import sys

def runExample():

    print("\nSparkFun Qwiic RFID Reader Example 1")
    myRFID = qwiic_rfid.QwiicRFID()

    if myRFID.begin() == False:
        print("\nThe Qwiic RFID Reader isn't connected to the system. Please check your connection", file=sys.stderr)
        return
    
    print("\nReady to scan some tags!")
    
    while True:
        val = input("\nEnter 1 to get tag ID and scan time: ")

        if int(val) == 1:
            print("\nGetting your tag ID...")
            tag = myRFID.getTag()
            print("\nTag ID: " + tag)

            scanTime = myRFID.getPrecReqTime()
            # If this time is too precise, try:
            # scanTime = myRFID.getReqTime()
            print("\nScan Time: " + str(scanTime))
        
        time.sleep(0.02)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
