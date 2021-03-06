

Installation
============

GIMIC requires CMake to configure and build. CMake is invoked via a front-end script called ``setup``::

  $ ./setup
  $ cd build
  $ make
  $ make install

To see all available options, run::

  $ ./setup --help

Branch "master"::
GIMIC requires CMake to configure and build.::

  $ mkdir build
  $ cd build
  $ cmake ../
  $ make
  $ make install

Test the installation with::

  $ make test


Parallelization
---------------

OpenMP parallelization is available::

  $ ./setup --omp

MPI parallelization is in the works.


Installation on Stallo supercomputer
------------------------------------

::

  $ git clone git@github.com:qmcurrents/gimic.git
  $ cd gimic
  $ module load Python/2.7.12-foss-2016b
  $ module load CMake/3.7.2-foss-2016b
  $ virtualenv venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt
  $ ./setup
  $ cd build
  $ make
  $ make install


Using BLAS1 and BLAS2 routines
------------------------------

With GNU compilers use::

  $ ./setup --blas

With Intel compilers and MKL use::

  $ ./setup --fc=ifort --cc=icc --cxx=icpc --cmake-options="-D ENABLE_MKL_FLAG=ON"
