# About gr-doa

gr-doa is a demonstration on the phase synchronization capability of Ettus Research's USRP X440. We provide apps to determine the accuracy of phase synchronization achieved and to estimate DoA which fundamentally requires accurate phase synchronization across the receive streams.

## Basic Dependencies

    UHD >= 4.8.0.0
    gnuradio >= 3.11.0.0
    armadillo >= 12.6.7

## Dependencies Needed for QA Testing

    octave (Tested 8.4.0)
    octave-signal (Tested 1.4.6)
    scipy (Tested 1.16.0)
    oct2py (Tested 5.8.0)

## What is implemented?

    - A wrapper to the USRP source block for a syncronised X440
    - Relative phase offset measurement and correction
    - Antenna element calibration for linear arrays
    - MUSIC algorithm for linear arrays
    - Root-MUSIC algorithm for linear arrays

## OSs Tested

    Ubuntu 24.04

## Installation

    $ git clone https://github.com/EttusResearch/gr-doa
    $ cd gr-doa
    $ mkdir build
    $ cd build
    $ cmake ..
    $ make
    $ make test
    $ sudo make install
    $ sudo ldconfig

## Documentation

    For a concise description of the steps involved: https://github.com/EttusResearch/gr-doa/wiki
    For detailed description: gr-doa/docs/whitepaper/doa_whitepaper.pdf
