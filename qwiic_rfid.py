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
import time

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
_AVAILABLE_I2C_ADDRESS = [0x13, 0x14]

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

    # Global struct
    # QUESTION: not really sure how to do this. Can you have a class within a class?
    # class rfidData(object):
    #     def __init__(self, tag, time):
    #         self.tag = tag
    #         self.time = time

    # Add temporary parameters
    # _libRfid = rfidData(0, "")
    # _libRfidArray = [None] * MAX_TAG_STORAGE

    RFID_TAG = None
    RFID_TIME = None
    TAG_ARRAY = [None] * MAX_TAG_STORAGE
    TIME_ARRAY = [None] * MAX_TAG_STORAGE

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
            :rtype: void
        """
        return qwiic_i2c.isDeviceConnected(self.address)

    # -------------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def begin(self):
        """
        Initialize the operation of the Qwiic GPIO
        
            :return: Returns true if the initialization was successful, otherwise False.
            :rtype: void
        """
        return self.isConnected()

    # --------------------------------------
    # getTag()
    #
    # This function gets the RFID tag from the Qwiic RFID Reader. If there is not
    # a tag then it will return an empty string. When the function is called the tag
    # is retrieved but saved to a global struct variable set within the _readTagTime
    # function. The tag is saved to a local variable, wiped from the global variable, and
    # local variable is returned. This allows me to get both the tag and the
    # associated time the tag was scanned at the same time, while keeping the 
    # function simple.
    def getTag(self):
        """
        Gets the current RFID tag

            :return: Returns the RFID tag
            :rtype: string
        """
        # Call the read command that will fill the global struct variable: rfidData
        self._readTagTime(self.TAG_AND_TIME_REQUEST)

        tempTag = self.RFID_TAG  # Assign the tag to our local variable
        self.RFID_TAG = None   # Clear the global variable
        return tempTag  # Return the local variable

    # --------------------------------------
    # getReqTime()
    # 
    # This funtion gets the time in seconds of the latest RFID tag was scanned from the Qwiic
    # RFID reader. If there is no tag then the time that is returned will be zero.
    # The information is received in the call to getTag() above, there is no time
    # without the variable and stored in the data member time of the struct rfidData.
    def getReqTime(self):
        """
        Gets the time when when RFID tag was last scanned

            :return: Returns time in seconds
            :rtype: int
        """
        # Global struct variable is loaded from getTag function. There is no time
        # without a tag scan.
        tempTime = self.RFID_TIME   # Assign the time to the local variable
        self.RFID_TIME = 0   # Clear the global variable
        return tempTime/1000    # Return the local variable in seconds

    # --------------------------------------------
    # getPrecReqTime()
    #
    # This function gets the precise time in seconds of the latest RFID tag was scanned from the Qwiic 
    # RFID reader. If there is no tag then the time that is returned will be zero.
    # The information is received in the call to getTag() above, there is no time
    # without the variable and stored in the data member time of the struct rfidData.
    def getPrecReqTime(self):
        """
        Gets the time when the RFID tag was last scanned

            :return: Returns time in seconds
            :rtype: int
        """
        # Global struct variable is loaded from getTag function. There is no time
        # without a tag scan.
        tempTime = float(self.RFID_TIME)/1000   # Assign the time to the local variable
        self.RFID_TIME = 0   # Clear the global variable
        return tempTime # Return the local variable in seconds
    
    # ---------------------------------------------
    # clearTags()
    #
    # This function clears the buffer from the Qwiic RFID reader by reading them
    # but not storing them.
    def clearTags(self):
        """
        Reads and clears the tags from the buffer

            :rtype: void - does not return anything
        """
        self._readAllTagsTimes(self.MAX_TAG_STORAGE)

    # --------------------------------------------
    # getAllTags(tagArray[MAX_TAG_STORAGE])
    #
    # This function gets all the available tags on the Qwiic RFID reader's buffer.
    # The buffer on the Qwiic RFID holds 20 tags and their scan time. Not knowing
    # how many are available until the i2c buffer is read, the parameter is a full
    # 20 element array.
    # def getAllTags(self, tagArray[self.MAX_TAG_STORAGE]):
    def getAllTags(self, tagArray):
        """
        Gets all the tags in the buffer

            :param tagArray: list of upto 20 RFID tag numbers
            :rtype: void - does not return anything
        """
        # Load up the global struct variables
        self._readAllTagsTimes(self.MAX_TAG_STORAGE)

        for i in range(0, self.MAX_TAG_STORAGE):
            tagArray[i] = self.TAG_ARRAY[i]  # Load up passed array with tag
            self.TAG_ARRAY[i] = ""   # Clear global variable

    # ---------------------------------------------
    # getAllPrecTimes(timeArray[MAX_TAG_STORAGE])
    # 
    # This function gets all the available precise scan times associated with the scanned RFID tags.
    # The buffer on the Qwiic RFID holds 20 tags and their scan time. Not knowing
    # how many are available until the I2C buffer is read, the parameter is a full 20 element
    # array.
    # A note on the time: the time is not the time of the day when the tage was scanned
    # but actually the time between when the tag was scanned and when it was read from the I2C bus.
    # def getAllPrecTimes(self, timeArray[self.MAX_TAG_STORAGE]):
    def getAllPrecTimes(self, timeArray):
    
        """
        Gets all times in the buffer

            :param timeArray: list of upto 20 times the RFID tag was read from the I2C bus
            :rtype: void - does not return anything
        """
        for i in range(0, self.MAX_TAG_STORAGE):
            timeArray[i] = self.TIME_ARRAY[i]    # Load up passed array with time in seconds
            timeArray[i] = float(timeArray[i])/1000
            self.TIME_ARRAY[i] = 0   # Clear global variable

    # ----------------------------------------------
    # changeAddress(newAddress)
    #
    # This function changes the I2C address of the Qwiic RFID. The address
    # is written to the memory location in EEPROM that determines its address.
    def changeAddress(self, newAddress):
        """
        Changes the I2C address of the Qwiic RFID reader

            :param newAddress: the new address to set the RFID reader to
            :rtype: bool
        """
        if newAddress < 0x07 or newAddress > 0x78:
            return false
        
        self._i2c.writeByte(self.address, self.ADDRESS_LOCATION, newAddress)
        
        self.address = newAddress

    # ------------------------------------------------
    # _readTagTime(_numofReads)
    # 
    # This function handles the I2C transaction to get the RFID tag and 
    # time from the Qwiic RFID reader. What comes in from the RFID reader is a 
    # number that was converted from a string to its direct numerical
    # representation which is then converted back to its original state. The tag
    # and the time is saves to the global rfidData struct.
    def _readTagTime(self, _numofReads):
        """
        Handles the I2C transaction to get the RFID tag and time

            :param _numofReads: int number of bytes to read
            :rtype: void - returns nothing
        """
        _tempTagStr = ""  
        _tempTime = 0

        # What is read from the buffer is immediately converted to a string and 
        # concatenated onto the temporary variable.
        _tempTagList = self._i2c.readBlock(self.address, 0, 10)
        
        for i in range(0, 6):
            _tempTagStr += str(_tempTagList[i])
        
        # The tag is copied to the tag data member of the rfidData struct
        self.RFID_TAG = _tempTagStr
        
        # Bring in the time
        if self.RFID_TAG == "000000":    # If the tag is blank

            # Time is zero if there is not a tag
            _tempTime = 0
        
        else:
            _tempTime = int(_tempTagList[6]) * 16 ** (6) + int(_tempTagList[7]) * 16 ** (4) + int(_tempTagList[8]) * 16 ** (2) + int(_tempTagList[9])
            
        # Time is copied to the time data member of the rfidData struct
        self.RFID_TIME = _tempTime   # Time in milliseconds

    # ----------------------------------------------------
    # _readAllTagsTimes(_numofReads)
    #
    # This function differs from the above by populating an array of 20 elements that
    # drains the entire available rfid buffer on the Qwiic RFID Reader. Similar to the
    # function above it handles the I2C transaction to get the RFID tags time from the 
    # Qwiic RFID Reader. What comes in the form of the RFID reader is a number that was
    # converted from a string to it's direct numerical representation which is then 
    # converted back to its' original state.
    def _readAllTagsTimes(self, _numofReads):
        """
        Populates an array of 20 RFID tags/times and drains available RFID buffer on the Reader.

            :param _numofReads: int number of bytes to read
            :rtype: void - returns nothing
        """        
        for i in range(0, _numofReads):
            _tempTagStr = ""
            _tempTime = 0
        
            # What is read from the buffer is immediately converted to a string and 
            # concatenated onto the temporary variable.
            _tempTagList = self._i2c.readBlock(self.address, 0, 10)
        
            for j in range(0, 6):
                _tempTagStr += str(_tempTagList[j])
        
            # The tag is copied to the tag data member of the rfidData class
            self.TAG_ARRAY[i] = _tempTagStr
            
            # Bring in the time but only if there is a tag
            if self.TAG_ARRAY[i] == "000000":    # Blank tag

                # Time is zero since there is no tag
                _tempTime = 0
            
            else:
                _tempTime = int(_tempTagList[6]) * 16 ** (6) + int(_tempTagList[7]) * 16 ** (4) + int(_tempTagList[8]) * 16 ** (2) + int(_tempTagList[9])
            
            # Time is copied to the time data member of the rfidData struct
            self.TIME_ARRAY[i] = _tempTime   # Convert to seconds            
