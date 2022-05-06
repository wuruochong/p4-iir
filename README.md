# IIR Filters in P4

## Introduction
This project contains proof of concept implementations of real time IIR filter calculations using P4 programmable switches.

3 separate implementations are available: 1st order, 2nd order, and 5th order IIR filters.

These implementations target the bmv2 software switch, v1model architecture. The switch is then emulated using Mininet. This setup allows for easy prototyping, debugging, and simulation without requiring a hardware programmable switch.

## Pre-requisites
Running this project requires a multitude of pre-requisite software that may be difficult to obtain, especially for some platforms.
### Recommended Process
I recommend using a VM image pre-packaged with all of the required P4 software available here: 

https://github.com/jafingerhut/p4-guide/blob/master/bin/README-install-troubleshooting.md

This project is verified to work using the 2022-Apr-02 "Release" VM build running in VirtualBox v6.1.32, although it will likely work with other VM versions in the link above running in a comparable virtual machine application.

Note that some of the python verification programs use packages such as numpy that are not included in these VMs. If you run into an error that a package is missing, simply use pip to install, e.g.:
```bash
> pip install numpy
```

This should provide the fastest and most reliable way to get this project running on your machine, *especially* if your machine is Windows or Mac based.
### Alternative Process
If you have a Linux based system, and you really want to avoid installing a VM, the same guide:

https://github.com/jafingerhut/p4-guide/blob/master/bin/README-install-troubleshooting.md

Provides instructions on manually installing the pre-requisite software to your machine.

## Workflow
Once you have obtained the pre-requisite environment, simply clone this repository onto your machine. Then navigate to a desired implementation e.g.:
```bash
> cd iir/1order
```
### Running the Implementation
To run the implementation, simply do:
```bash
> make
```
This will compile the implementation then automatically launch the mininet emulation environment. Notice that your terminal is now the mininet terminal. Now, open a separate terminal for one of the emulated devices on the network, `h1`:
```bash
mininet> xterm h1
```
A new terminal for `h1` should have popped up. You can now command `h1` to run the driver program in this new terminal:
```bash
> python3 driver.py
```
The program should now prompt you for filter coefficients, input them as you see fit. 

Then it will prompt you for a csv containing filter inputs. One is provided in the implementation (`ecg.csv`), feel free to try your own.

Finally, it will prompt you to input a filename to store the filter outputs, e.g. `ecg_out.csv`.

The driver program will now run, feeding the entered coefficients and input data to the switch, and recording the switch outputs to the designated file.

Once it is done, `exit` the `h1` xterm, `exit` the mininet terminal, and you should be back with your default terminal at the implementation directory. `make stop` to stop mininet running in the background.

### Running the verifier
`verifier.py` contains a python program that will do the same calculation done by the switch, but with full floating point arithmetic. This can be used to get a "reference" output that can be compared against the switch output. `verifier.py` requires you to enter the input csv, output csv, and filter coefficients as command line arguments.
```bash
> python3 verifier.py
Usage: python verifier.py [input csv] [output csv] [b0]
```
to get the exact order of inputs. Then run `verifier.py` with the correct inputs.
```bash
> python3 verifier.py ecg.csv ecg_out_reference.csv 0.5
```
This will produce the reference output for `ecg.csv` in `ecg_out_reference.csv` using filter coefficient `b0=0.5`.

### Comparing output results
Once the implementation and verifier have both been run for the same input dataset and coefficient set, you can now compare the results. Run
```bash
> python3 errorCalc.py ecg_out_reference.csv ecg_out.csv
```
and it will calculate the average and maximum percent errors of the switch results vs. the reference result.

### Cleaning up
`make clean` to clean up the directory.