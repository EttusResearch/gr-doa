## Folder Organization

- **Narrowband-Flowgraphs/**: Main flowgraphs for narrowband DoA experiments and calibration.
- **Narrowband-Flowgraphs/phase_offset_measurement_correction/**: Flowgraphs for phase offset measurement and correction.
- **WiFi-Flowgraphs/**: Flowgraphs for WiFi-based DoA experiments and calibration.
- **debugging/**: General-purpose debugging and test flowgraphs.
- **simulations/**: Simulation flowgraphs for algorithm validation.
- **testdata/**: Scripts and folders for storing and processing test data.

---

### Simulation Flowgraphs (simulations/)
 - `simulations/run_MUSIC_lin_array_simulation.grc`: Execute this flowgraph to see a simulation setup of two-target tracking using MUSIC algorithm with an ideal uniform linear array.
 - `simulations/run_RootMUSIC_lin_array_simulation.grc`: Execute this flowgraph to see a simulation setup of two-target tracking using Root-MUSIC algorithm with an ideal uniform linear array.
 - `simulations/run_calib_lin_array_simulation.grc`: Execute this flowgraph to see a simulation setup involving the calibration of a non-ideal uniform linear array.
 - `simulations/run_MUSIC_calib_lin_array_simulation.grc`: Execute this flowgraph to see a simulation setup of two-target tracking using MUSIC algorithm with a calibrated uniform linear array. It is required that `simulations/run_calib_lin_array_simulation.grc` is run first which saves a config file to be used by this flowgraph.
 - `simulations/run_RootMUSIC_calib_lin_array_simulation.grc`: Execute this flowgraph to see a simulation setup of two-target tracking using Root-MUSIC algorithm with a calibrated uniform linear array. It is required that `simulations/run_calib_lin_array_simulation.grc` is run first which saves a config file to be used by this flowgraph.


### Flowgraphs to Run Experiments with an X440
 - `Narrowband-Flowgraphs/phase_offset_measurement_correction/run_DoA_transmitter.grc`: Run this flowgraph to transmit a tone.
 - `Narrowband-Flowgraphs/phase_offset_measurement_correction/estimate_constant_phase_offsets_and_save.grc`: The first flowgraph to be run at the host PC in order to store the constant repeatable relative phase offsets in a config file. Refer to the wiki page or the whitepaper for more details on the calibration setup.
 - `Narrowband-Flowgraphs/phase_offset_measurement_correction/view_op_with_corrected_phase_offsets.grc`: Run this flowgraph to view the phase-corrected receive streams.
 - `Narrowband-Flowgraphs/phase_offset_measurement_correction/calculate_phase_sync_accuracy.grc`: Run this flowgraph to store the phase misalignment values post-correction in a config file.
 - `Narrowband-Flowgraphs/run_MUSIC_lin_array.grc`: Execute this flowgraph to track one target transmitter using MUSIC algorithm with an uncalibrated uniform linear array.
 - `Narrowband-Flowgraphs/run_RootMUSIC_lin_array.grc`: Execute this flowgraph to track one target transmitter using Root-MUSIC algorithm with an uncalibrated uniform linear array.
 - `Narrowband-Flowgraphs/calibrate_lin_array.grc`: Run this flowgraph to calibrate a uniform linear array.
 - `Narrowband-Flowgraphs/run_MUSIC_calib_lin_array.grc`: Run this flowgraph to track one target transmitter using MUSIC algorithm with a calibrated uniform linear array.
 - `Narrowband-Flowgraphs/run_RootMUSIC_calib_lin_array.grc`: Run this flowgraph to track one target transmitter using Root-MUSIC algorithm with a calibrated uniform linear array.

### Phase Offset Measurement & Correction (Narrowband-Flowgraphs/phase_offset_measurement_correction/)
- `run_DoA_transmitter.grc`: Run this flowgraph to transmit a tone.
- `estimate_constant_phase_offsets_and_save.grc`: Store constant repeatable relative phase offsets in a config file.
- `view_op_with_corrected_phase_offsets.grc`: View the phase-corrected receive streams.
- `calculate_phase_sync_accuracy.grc`: Store phase misalignment values post-correction in a config file.

### WiFi Flowgraphs (WiFi-Flowgraphs/)
- `calibrate_lin_array_WiFi.grc`: Calibrate a uniform linear array for WiFi signals.
- `run_DoA_receiver_WIFI.grc`: Run the DoA receiver for WiFi experiments.
- `run_DoA_transmitter_WIFI.grc`: Run the DoA transmitter for WiFi experiments.
- `run_MUSIC_calib_lin_array_WiFi.grc`: MUSIC algorithm with a calibrated array (WiFi).
- `run_MUSIC_lin_array_WiFi.grc`: MUSIC algorithm with an uncalibrated array (WiFi).
- `simulations/run_MUSIC_lin_array_simulation_WiFi.grc`: Simulate MUSIC algorithm for WiFi.

### Debugging Flowgraphs (debugging/)
- `debugging/rx_general_test.grc`: An easy way to check if your source is transmitting (e.g. X310, Walkie-talkie, etc.).
- `debugging/X440_indiv_channel_test.grc`: Shows all 4 Channels Spectrum & Waterfall to see if there are any disruptions in the signal.
- `WiFi-Flowgraphs/debugging/test_detection_WiFi.grc`: Debug/test WiFi detection.
- `WiFi-Flowgraphs/debugging/run_DoA_receiver_WiFi.grc`: Debug/test WiFi Power detection
