Qwiic_RFID_Py
===============

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic-rfid/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun-qwiic-rfid.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_RFID_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_RFID_Py.svg" /></a>
	<a href="https://qwiic-rfid-py.readthedocs.io/en/latest/?" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-rfid-py/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_RFID_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>

</p>

<img src="https://cdn.sparkfun.com/assets/parts/1/3/6/1/0/15191-SparkFun_RFID_Qwiic_Reader-01a.jpg"  align="right" width=300 alt="SparkFun Qwiic RFID Reader">

Python module for the [SparkFun RFID Qwiic Reader](https://www.sparkfun.com/products/15191)

This module is also compatible with the following products:
* [SparkFun RFID Qwiic Kit](https://www.sparkfun.com/products/15209)

This python package is a port of the existing [SparkFun Qwiic RFID Reader Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_RFID_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

## Contents

* [Supported Platforms](#supported-platforms)
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Documentation](#documentation)
* [Example Use](#example-use)

Supported Platforms
--------------------
The Qwiic RFID Python package current supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)
* [NVidia Jetson Nano](https://www.sparkfun.com/products/15297)
* [Google Coral Development Board](https://www.sparkfun.com/products/15318)

Dependencies
--------------
This driver package depends on the qwiic I2C driver:
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun Qwiic RFID module documentation is hosted at [ReadTheDocs](https://qwiic-rfid-py.readthedocs.io/en/latest/?)

Installation
---------------
### PyPi Installation

This repository is hosted on PyPi as the [sparkfun-qwiic-rfid](https://pypi.org/project/sparkfun-qwiic-rfid/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic-rfid
```
For the current user:

```sh
pip install sparkfun-qwiic-rfid
```
To install, make sure the setuptools package is installed on the system.

Direct installation at the command line:
```sh
python setup.py install
```

To build a package for use with pip:
```sh
python setup.py sdist
 ```
A package file is built and placed in a subdirectory called dist. This package file can be installed using pip.
```sh
cd dist
pip install sparkfun-qwiic-rfid-<version>.tar.gz
```

Example Use
 -------------
See the examples directory for more detailed use examples.

```python
from __future__ import print_function
import qwiic_rfid
import time
import sys

def run_example():

    print("\nSparkFun Qwiic RFID Reader Example 1")
    my_RFID = qwiic_rfid.Qwiic_RFID()

    if my_RFID.begin() == False:
        print("\nThe Qwiic RFID Reader isn't connected to the system. Please check your connection", file=sys.stderr)
        return
    
    print("\nReady to scan some tags!")
    
    while True:
        val = input("\nEnter 1 to get tag ID and scan time: ")

        if int(val) == 1:
            print("\nGetting your tag ID...")
            tag = my_RFID.get_tag()
            print("\nTag ID: " + tag)

            scan_time = my_RFID.get_prec_req_time()
            # If this time is too precise, try:
            # scan_time = my_RFID.get_req_time()
            print("\nScan Time: " + str(scan_time))
        
        time.sleep(0.02)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)

```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
