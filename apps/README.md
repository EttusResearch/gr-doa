### Simulation Flowgraphs
 - `run_MUSIC_lin_array_simulation.grc`: Execute this flowgraph to see a simulation
 setup of two-target tracking using MUSIC algorithm with an ideal uniform linear array.
 - `run_RootMUSIC_lin_array_simulation.grc`: Execute this flowgraph to see a simulation
 setup of two-target tracking using Root-MUSIC algorithm with an ideal uniform linear array.
 - `run_calib_lin_array_simulation.grc`: Execute this flowgraph to see a simulation
 setup involving the calibration of a non-ideal uniform linear array.
 - `run_MUSIC_calib_lin_array_simulation.grc`: Execute this flowgraph to see a simulation
 setup of two-target tracking using MUSIC algorithm with a calibrated uniform linear array.
 It is required that `run_calib_lin_array_simulation.grc` is run first which saves a config file 
 to be used by this flowgraph.
 - `run_RootMUSIC_calib_lin_array_simulation.grc`: Execute this flowgraph to see a simulation
 setup of two-target tracking using Root-MUSIC algorithm with a calibrated uniform linear array.
 It is required that `run_calib_lin_array_simulation.grc` is run first which saves a config file 
 to be used by this flowgraph.


### Flowgraphs to Run Experiments with an X440
 - `rx_general_test.grc`: An easy way to check if your source is transmitting (e.g. X310, Walkie-talkie, etc.).
 - `X440_indiv_channel_test.grc`: Shows all 4 Channels Spectrum & Waterfall to see if there are any disruptions in the signal. 
 - `run_DoA_transmitter.grc`: Run this flowgraph to transmit a tone. 
 - `estimate_constant_phase_offsets_and_save.grc`: The first flowgraph to be run at 
 the host PC in order to store the constant repeatable relative phase offsets in a config file. 
 Refer to the wiki page or the whitepaper for more details on the calibration setup.
 - `view_op_with_corrected_phase_offsets.grc`: Run this flowgraph to view the 
 phase-corrected receive streams. 
 - `calculate_phase_sync_accuracy.grc`: Run this flowgraph to store the phase misalignment
 values post-correction in a config file. 
 - `run_MUSIC_lin_array.grc`: Execute this flowgraph to track one target transmitter 
 using MUSIC algorithm with an uncalibrated uniform linear array.
 - `run_RootMUSIC_lin_array.grc`: Execute this flowgraph to track one target transmitter 
 using Root-MUSIC algorithm with an uncalibrated uniform linear array.
 - `calibrate_lin_array.grc`: Run this flowgraph to calibrate a uniform linear array.
 - `run_MUSIC_calib_lin_array.grc`: Run this flowgraph to track one target transmitter 
 using MUSIC algorithm with a calibrated uniform linear array.
 - `run_RootMUSIC_calib_lin_array.grc`: Run this flowgraph to track one target transmitter 
 using Root-MUSIC algorithm with a calibrated uniform linear array. 
