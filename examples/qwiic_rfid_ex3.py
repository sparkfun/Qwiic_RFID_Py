# !/usr/bin/env python
# ----------------------------------------------------------------
# qwiic_rfid_ex3.py
#
# Example that takes user input to change the I2C address of Qwiic RFID
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
# This example code demonstrates how to change the address of the Qwiic RFID Tag
# Reader to one of your choosing. There is a set range of available addresses from
# 0x07 to 0x78, so make sure your chosen address falls within this range.

from __future__ import print_function
import qwiic_i2c
import qwiic_rfid
import time
import sys

def runExample():

    print("\nSparkFun Qwiic RFID Reader Example 3")
    myRFID = qwiic_rfid.QwiicRFID()

    if myRFID.isConnected() == False:
        print("\nThe Qwiic RFID Reader isn't connected to the system. Please check your connection", file=sys.stderr)
        return
    
    myRFID.begin()
    print("\nReady!")

    print("\nEnter a new I2C address for the Qwiic RFID Reader to use.")
    print("\nDon't use the 0x prefix. For instance if you wanted to")
    print("\nchange the address to 0x5B, you would type 5B and hit enter.")

    newAddress = input("\nNew Address: ")
    int(newAddress, 16)

    # Check if the user entered a valid address
    if newAddress > 0x08 and newAddress < 0x77:
        print("\nCharacters received and new address valid!")
        print("\nAttempting to set RFID reader address...")
        
        if myRFID.changeAddress(newAddress) == True:
            print("\nAddress successfully changed!")
            # Check that the RFID Reader acknowledges on new address
            if myRFID.isConnected() == False:
                print("\nThe Qwiic RFID Reader isn't connected to the system. Please check your connection", file=sys.stderr)

        else:
            print("\nAddress change was not successful")
    
    else: 
        print("\nAddress entered not a valid I2C address")
    
    # I2C Scanner
    addressesOnBus = qwiic_i2c.scan()
    while 1:

        if not addressesOnBus:
            print("\nNo devices found on I2C bus.")

        else: 
            for i in range(0, len(addressesOnBus)):
                print("\I2C device found at address: 0x" + hex(addressesOnBus[i]))

        # Delay for 5 seconds
        time.sleep(5)

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)