# About gr-doa
gr-doa is a demonstration on the phase synchronization capability of Ettus Research's TwinRX daughtercards. 
TwinRX daughtercards can achieve a high degree of accurate phase synchronization except for constant 
repeatable relative phase offsets. We provide apps to determine the accuracy of phase synchronization achieved 
and to estimate DoA which fundamentally requires accurate phase synchronization 
across the receive streams.

### Basic Dependencies
 - UHD >= 3.10.1.0
 - gnuradio >= 3.7.10.1
 - armadillo >= 7.300

### Dependencies Needed for QA Testing
 - octave (Tested 4.0.2)
 - octave-signal (Tested 1.3.2)
 - scipy (Tested 0.15.1)
 - oct2py (Tested 3.5.9)

### Dependencies Needed for Doc
 - texlive-latex-base

### What is implemented?
 - A wrapper to the USRP source block when using an X310 with 1 or 2 TwinRXs
 - Relative phase offset measurement and correction
 - Antenna element calibration for linear arrays
 - MUSIC algorithm for linear arrays
 - Root-MUSIC algorithm for linear arrays 

### OSs Tested 
 - Ubuntu 14.04, Ubuntu 16.04 
 
### Installation
`$ git clone https://github.com/EttusResearch/gr-doa` <br />
`$ cd gr-doa` <br />
`$ mkdir build` <br />
`$ cd build` <br />
`$ cmake ..` <br />
`$ make` <br />
`$ make test` <br />
`$ sudo make install` <br />
`$ sudo ldconfig` <br />

### Documentation
 - For a concise description of the steps involved: `https://github.com/EttusResearch/gr-doa/wiki`
 - For details about the blocks available
in this package: `gr-doa/build/docs/doxygen/html/index.html`
 - For detailed description: `gr-doa/docs/whitepaper/doa_whitepaper.pdf`
