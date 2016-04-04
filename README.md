# python-quartus
[Quartus Prime](https://www.altera.com/products/design-software/fpga-design/quartus-prime/overview.html) is a software suite for compiling Verilog and VHDL for Altera (now part of Intel) devices. Unfortunately, most scripts for automating compilation and interaction are written in Tcl, and no one wants that.

This project aims to allow interaction with the quartus libraries via python.

## Installation

### Windows

Download and install [Quartus Prime](https://www.altera.com/products/design-software/fpga-design/quartus-prime/overview.html). Add 
*C:\altera_lite\15.1\quartus\bin64* to the system %PATH%.

Then clone this repo and run the command:

```
python setup.py install
```

#### Linux

Download and install [Quartus Prime](https://www.altera.com/products/design-software/fpga-design/quartus-prime/overview.html)
