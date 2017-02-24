[![Build Status](https://travis-ci.org/qmcurrents/gimic.svg?branch=master)](https://travis-ci.org/qmcurrents/gimic/builds)

- [Documentation](http://gimic.readthedocs.io) (currently empty)

This is the GIMIC program for calculating magnetically induced currents in
molecules. For this program produce any kind of useful information, you
need to provide it with an AO density matrix and three (effective)
magnetically perturbed AO density matrices in the proper format. Currently
only recent versions of ACES2 and Turbomole can produce these matrices, but
Dalton is in the works. If you would like to add your favourite program to the
list please use the source, Luke.

- For instructions how to compile and install this program refer to
  the INSTALL file in the top level directory.
- For more detailed information on how to use the program read the documents
  found in the Documentation directory.
- There is an annotated example input in the examples/ directory.
- For information on command line flags available run: 'gimic --help'

To run gimic you need to have at least three files: The gimic input file
(gimic.inp), the compound density file (XDENS) and the compound basis set and
structure file (mol). Copy the example gimic.inp to your work directory and
edit to your needs. To produce the mol and XDENS files:

- CFOUR: Do a normal NMR calculation and then run the 'xcpdens' program
  distributed with GIMIC to make the XDENS file. Then run the MOL2mol.sh
  script to produce the mol file.

- Turbomole: Add the $gimic keyword to the control file and then run mpshift
  as normal to produce a XDENS file. Then run the turbo2mol.py script to
  create the mol file from the coord and basis files.

Before doing the actual calculation it might be a good idea to check that the
grids are correct, run:

```shell
$ gimic --dryrun
```

and examine the .xyz files that GIMIC produces. If they look ok, simply run

```shell
$ gimic
```

If you want to run the parallel version, there is a wrapper script called
'qgimic' (see qgimic --help for a list of command line options) to produce a
generic run script for most queueing systems. Eg. to set up a parallel
calculation with 8 CPUs, 1 h time and 200 MB memory to be run in /work/slask

```shell
$ qgimic -n 8 -t 01:00 -m 200 /work/slask
```

This produces a 'gimic.run' file. Edit this file and make sure it's ok, and
then submit it to the queueing system:

```shell
$ qsub gimic.run
```

That's it! May the foo be with you!
