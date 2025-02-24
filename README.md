**ChipTools** is a utility to automate FPGA build and verification

[![Documentation Status](https://readthedocs.org/projects/chiptools/badge/?version=latest)](http://chiptools.readthedocs.org/en/latest/?badge=latest)

## What can it do?

ChipTools aims to simplify the process of building and testing FPGA designs by
providing a consistent interface to vendor applications and automating simulation and synthesis flows.

### Key features

   * Seamlessly switch between vendor applications without modifying build scripts or project files.
   * Enhance testbenches with Python based stimulus generation and checking.
   * Automate test execution and reporting using the Python Unittest framework.
   * Automatically check and archive build outputs.
   * Preprocess and update files before synthesis to automate tasks such as updating version registers.
   * Free and open source under the [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0).

## Getting Started
```
  # Clone the ChipTools repository to your system
  $ git clone https://github.com/pabennett/chiptools.git
  
  # Install using the setup.py script provided in the root directory
  $ python setup.py install
  
  # Start the ChipTools command line interface
  $ chiptools
```
Refer to the [documentation](http://chiptools.readthedocs.org/en/latest/examples.html) for examples on using ChipTools to simulate and build FPGA designs.

## Supported Tools

The following tools are currently supported, support for additional tools
will be added in the future. 

### Simulation Tools

* Modelsim (tested with 10.3)
* ISIM (tested with 14.7)
* GHDL (tested with 0.31)

### Synthesis Tools

* Xilinx ISE (tested with 14.7)
* Quartus (tested with 13.1)
* Vivado (tested with 2015.4)

