#-----------------------------------------------------------------------------
# qwiic_rfid.py
#
# Python library for the SparkFun qwiic rfid reader.
#   https://www.sparkfun.com/products/15191
#
#------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, December 2020
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem 
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#==================================================================================
# Copyright (c) 2020 SparkFun Electronics
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

"""
qwiic_rfid
============
Python module for the Qwiic RFID Reader.

This python package is a port of the existing [SparkFun Qwiic RFID Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_RFID_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

"""
#-----------------------------------------------------------------------------

import qwiic_i2c

# Define the device name and I2C addresses. These are set in teh class definition
# as class variables, making them available without having to create a class instance.
# This allows higher level logic to rapidly create an index of qwiic devices at
# runtime.
#
# The name of this device
_DEFAULT_NAME = "Qwiic RFID"

# Some devices have multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x7D, 0x7C]

# QUESTION: what do you do if the i2c address is software configurable?!

# define the class that enxapsulates the device being created. All information associated with this
# device is enxapsulated by this class. The device class should be the only value exported
# from this module.

class QwiicRFID(object):
    """
    QwiicRFID

        :param address: The I2C address to use for the device.
                        If not provied, the default address is  used.
        :param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.
        :return: The RFID device object.
        :rtype: Object
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Global variables
    ALTERNATE_ADDR = 0x7C
    ADDRESS_LOCATION = 0xC7

    TAG_AND_TIME_REQUEST = 10
    MAX_TAG_STORAGE = 20
    BYTES_IN_BUFFER = 4

    # Constructor
    def __init__(self, address=None, i2c_driver=None):
        
        # Did the user specify an I2C address?
        self.address = address if address != None else self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver == None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c == None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

    # ------------------------------------
    # isConnected()
    #
    # Is an actual board connected to our system?
    def isConnected(self):
        """
        Determine if a Qwiic RFID device is connected to the system.

            :return: True if the device is connected, otherwise False.
            :rtype: bool
        """
        return qwiic_i2c.isDeviceConnected(self.address)
