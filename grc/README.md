# GNU Radio DOA (Direction of Arrival) Blocks Documentation

This document provides comprehensive documentation for all blocks in the GNU Radio DOA module, including their functionality, parameters, and usage guidelines.

## Table of Contents
- [Source Blocks](#source-blocks)
- [Calibration Blocks](#calibration-blocks)
- [DOA Algorithm Blocks](#doa-algorithm-blocks)
- [Utility Blocks](#utility-blocks)
- [Output Blocks](#output-blocks)

---

## Source Blocks

### X440 USRP Source
**Block ID:** `doa_x440_usrp_source`

A specialized USRP source block optimized for X440 devices in DOA applications.

#### Functionality
This block provides a wrapper around the standard USRP source block with X440-specific optimizations. It supports multiple synchronized channels essential for direction finding applications.

#### Parameters
- **Samp Rate** (`samp_rate`): Sets the sampling frequency for all channels. Higher rates provide more bandwidth but require more processing power.
  
- **Center Freq** (`center_freq`): The RF frequency you want to receive. This should match the frequency of the signals you're trying to locate.
  
- **Gain Value** (`gain`): Controls the receiver sensitivity. Higher gain amplifies weak signals but may cause strong signals to saturate.
  
- **Num Channels** (`sources`): Number of antenna elements to use simultaneously. More channels improve DOA accuracy but increase computational load.
  
- **Device Address** (`addresses`): Network location of your USRP device. Change this to match your device's IP address.
  
- **Device Args** (`device_args`): Additional hardware configuration options like master clock rate for precise timing synchronization between channels.

#### Outputs
- **out**: Synchronized complex baseband data from each antenna channel, essential for phase-coherent DOA processing.

---

## Calibration Blocks

### Calibrate Linear Array
**Block ID:** `doa_calibrate_lin_array`

Calibrates a uniform linear antenna array using a known pilot signal.

#### Functionality
This block compensates for hardware differences between antenna channels by using a reference signal at a known angle. It's essential for accurate DOA estimation.

#### Parameters
- **Normalized Spacing** (`norm_spacing`): Physical distance between antenna elements divided by signal wavelength. This determines the array's angular resolution and potential for spatial aliasing.
  
- **Num Ant Elements** (`num_ant_ele`): Total number of antennas in your array. More elements provide better resolution and accuracy.
  
- **Pilot Angle** (`pilot_angle`): The exact angle where you've placed a known reference transmitter. This must be measured accurately for proper calibration.

### Phase Offset Estimation
**Block ID:** `doa_phase_offset_est`

Estimates phase differences between antenna channels caused by hardware mismatches.

#### Functionality
Measures how much each channel's phase differs from the first channel. These offsets must be corrected for accurate DOA estimation.

#### Parameters
- **Num. Inputs** (`num_inputs`): Number of antenna channels to compare. Should match your antenna array size.
  
- **Skip Ahead** (`n_skip_ahead`): Number of initial samples to ignore while the hardware stabilizes. Prevents estimation errors from startup transients.

### Phase Correction Hierarchy
**Block ID:** `doa_phase_correct_hier`

Applies previously measured phase corrections to incoming data.

#### Functionality
Uses stored calibration data to remove phase differences between channels, ensuring all antennas appear to have identical phase response.

#### Parameters
- **Num Ports** (`num_ports`): Number of channels to correct simultaneously.
  
- **Config File** (`config_filename`): Location of the file containing your measured phase corrections.

### Antenna Correction
**Block ID:** `doa_antenna_correction`

Normalizes both gain and phase differences between antenna elements.

#### Functionality
Applies comprehensive corrections to make all antenna channels behave identically, compensating for both amplitude and phase variations.

#### Parameters
- **Num Antenna Elements** (`num_ant_ele`): Number of channels in your antenna array.
  
- **Config File** (`config_filename`): File containing the measured gain and phase corrections for each antenna.

---

## DOA Algorithm Blocks

### MUSIC Linear Array
**Block ID:** `doa_MUSIC_lin_array`

Implements the MUSIC algorithm for high-resolution direction finding.

#### Functionality
Uses eigenvalue decomposition to separate signal and noise, then searches for directions where the noise is orthogonal to incoming signals. Produces a spectrum with sharp peaks at signal directions.

#### Parameters
- **Normalized Spacing** (`norm_spacing`): Antenna spacing relative to wavelength. Must be ≤0.5 to avoid ambiguous results.
  
- **Num Targets** (`num_targets`): How many separate signal sources you expect to detect simultaneously.
  
- **Num Ant Elements** (`inputs`): Size of your antenna array. Must be larger than the number of targets.
  
- **P-Spectrum Length** (`pspectrum_len`): Resolution of the output angle spectrum. Higher values give more precise angle estimates.

### Root-MUSIC Linear Array
**Block ID:** `doa_rootMUSIC_linear_array`

Advanced version of MUSIC that finds angles by solving polynomials instead of searching spectra.

#### Functionality
More computationally efficient than standard MUSIC and often more accurate, especially for signals arriving from the sides of the array.

#### Parameters
- **Normalized Spacing** (`norm_spacing`): Same spacing considerations as MUSIC - keep ≤0.5 for unambiguous results.
  
- **Num Targets** (`num_targets`): Number of simultaneous signals to locate.
  
- **Num Inputs** (`num_ant_ele`): Antenna array size, must exceed target count.

---

## Utility Blocks

### Autocorrelate
**Block ID:** `doa_autocorrelate`

Creates correlation matrices that DOA algorithms need to separate signals from noise.

#### Functionality
Computes how signals from different antennas relate to each other over time. This statistical information is what allows MUSIC and similar algorithms to work.

#### Parameters
- **Num Inputs** (`inputs`): Number of antenna channels to correlate.
  
- **Snapshot Size** (`snapshot_size`): How many samples to use for each correlation estimate. Larger values give better statistics but slower updates.
  
- **Overlap Size** (`overlap_size`): How much consecutive correlation estimates overlap. Provides smoother results with some computational cost.
  
- **Averaging Method** (`avg_method`): Forward-Backward averaging can improve performance by exploiting signal symmetries.

### Find Local Maximum
**Block ID:** `doa_find_local_max`

Extracts angle estimates from DOA algorithm output spectra.

#### Functionality
Locates the peaks in MUSIC pseudo-spectra and converts peak positions to actual angle measurements.

#### Parameters
- **Num. Max. Values** (`num_max_vals`): How many peaks (signal directions) to find and report.
  
- **Vector Len.** (`vector_len`): Size of the input spectrum from the DOA algorithm.
  
- **X min/X max** (`x_min`, `x_max`): Angular range to search within. Typically covers your antenna's field of view.

---

## Output Blocks

### Serial Connection
**Block ID:** `doa_serial_connection`

Sends angle measurements to external devices like servo controllers for antenna tracking.

#### Functionality
Converts DOA results into serial commands that microcontrollers can use to point antennas or other devices toward detected signals.

#### Parameters
- **Serial Port** (`port`): Which serial port connects to your control hardware.
  
- **Baud Rate** (`baudrate`): Communication speed with the external device. Must match the receiver's settings.
  
- **Data Format** (`data_format`): How to format the angle data for transmission.
  
- **Num of Targets** (`num_max`): How many target directions to send simultaneously.
  
- **Debug Output** (`debug`): Shows transmitted data on screen for troubleshooting.

### Save Antenna Calibration
**Block ID:** `doa_save_antenna_calib`

Records antenna calibration measurements for later use.

#### Functionality
Takes ongoing calibration estimates and creates stable, averaged correction values that can be applied to future measurements.

#### Parameters
- **Num Inputs** (`num_inputs`): Number of antennas being calibrated.
- **Samples To Average** (`samples_to_average`): How many measurements to combine for stable calibration values.
- **Config Filename** (`config_filename`): Where to store the final calibration data.

### Average and Save
**Block ID:** `doa_average_and_save`

Creates stable measurements by averaging multiple samples before saving.

#### Parameters
- **Num Inputs** (`num_inputs`): Number of data streams to average.
- **Samples To Average** (`samples_to_average`): Size of averaging window for noise reduction.
- **Config File** (`config_filename`): Output location for averaged results.

### Find Maximum and Save
**Block ID:** `doa_findmax_and_save`

Identifies peak values in data streams and stores them for calibration purposes.

#### Parameters
- **Num Inputs** (`num_inputs`): Number of input data streams.
- **Samples To Find Max.** (`samples_to_findmax`): How many samples to examine when finding peak values.
- **Config File** (`config_filename`): Where to save the identified maximum values.

---

## Usage Guidelines

### Typical DOA Processing Chain

1. **Signal Acquisition**: Use X440 USRP Source with synchronized channels
2. **Calibration**: Apply phase corrections and antenna calibration
3. **Correlation**: Generate correlation matrices using Autocorrelate block
4. **DOA Estimation**: Apply MUSIC or Root-MUSIC algorithms
5. **Peak Detection**: Use Find Local Max to extract angle estimates
6. **Output**: Send results via Serial Connection or save to file

### Parameter Selection Guidelines

#### Array Spacing
- Use d = λ/2 (norm_spacing = 0.5) for optimal performance
- Smaller spacing reduces spatial aliasing but may decrease resolution
- Larger spacing (>λ/2) causes ambiguities

#### Snapshot Size
- Larger snapshots improve statistical accuracy
- Trade-off with processing latency and tracking speed
- Typical range: 512-4096 samples

#### Number of Elements vs. Targets
- Always ensure: num_ant_elements > num_targets
- More elements improve resolution and accuracy
- Minimum: 3 elements for 2D DOA estimation

### Performance Considerations

- **Computational Complexity**: MUSIC O(N³), Root-MUSIC O(N²) where N = array elements
- **Memory Usage**: Correlation matrices require N² complex storage
- **Accuracy**: Improves with SNR, snapshot length, and array aperture
- **Resolution**: Limited by array geometry and algorithm choice

---

## Troubleshooting

### Common Issues

1. **Poor DOA Accuracy**
   - Check array calibration
   - Verify element spacing
   - Increase snapshot size
   - Ensure sufficient SNR

2. **Ambiguous Results**
   - Reduce element spacing
   - Check for spatial aliasing
   - Verify target count parameter

3. **Calibration Problems**
   - Ensure pilot source is at known angle
   - Check phase stability
   - Verify timing synchronization

### Error Messages

- "num_ant_ele must be > num_targets": Increase array elements or reduce target count
- "norm_spacing must be ≤ 0.5": Reduce element spacing or increase frequency
- "overlap_size must be < snapshot_size": Adjust overlap parameter
Converts GNU Radio float data to serial commands for controlling servo motors based on DOA estimates. Useful for implementing tracking systems.

#### Parameters
- **Serial Port** (`port`): Device path
  - Type: String
  - Default: "/dev/ttyUSB0"
  - Platform: Linux/Unix format
  
- **Baud Rate** (`baudrate`): Communication speed
  - Type: Integer
  - Default: 115200
  - Options: 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600
  
- **Data Format** (`data_format`): Output format
  - Options: "csv" (Comma-Separated Values)
  
- **Num of Targets** (`num_max`): Expected number of targets
  - Type: Integer
  - Default: 1
  
- **Debug Output** (`debug`): Enable console debugging
  - Type: Boolean
  - Default: False

### Save Antenna Calibration
**Block ID:** `doa_save_antenna_calib`

Stores calibration results to configuration files.

#### Functionality
Averages calibration estimates over multiple samples and saves gain and phase corrections for later use.

#### Parameters
- **Num Inputs** (`num_inputs`): Number of antenna elements
- **Samples To Average** (`samples_to_average`): Averaging window size
- **Config Filename** (`config_filename`): Output file path

### Average and Save
**Block ID:** `doa_average_and_save`

Averages input streams and stores results.

#### Parameters
- **Num Inputs** (`num_inputs`): Number of input streams
- **Samples To Average** (`samples_to_average`): Averaging window
- **Config File** (`config_filename`): Output file path

### Find Maximum and Save
**Block ID:** `doa_findmax_and_save`

Finds maximum values in input streams and saves results.

#### Parameters
- **Num Inputs** (`num_inputs`): Number of input streams
- **Samples To Find Max.** (`samples_to_findmax`): Sample window for maximum search
- **Config File** (`config_filename`): Output file path

---

## Usage Guidelines

### Typical DOA Processing Chain

1. **Signal Acquisition**: Use X440 USRP Source with synchronized channels
2. **Calibration**: Apply phase corrections and antenna calibration
3. **Correlation**: Generate correlation matrices using Autocorrelate block
4. **DOA Estimation**: Apply MUSIC or Root-MUSIC algorithms
5. **Peak Detection**: Use Find Local Max to extract angle estimates
6. **Output**: Send results via Serial Connection or save to file

### Parameter Selection Guidelines

#### Array Spacing
- Use d = λ/2 (norm_spacing = 0.5) for optimal performance
- Smaller spacing reduces spatial aliasing but may decrease resolution
- Larger spacing (>λ/2) causes ambiguities

#### Snapshot Size
- Larger snapshots improve statistical accuracy
- Trade-off with processing latency and tracking speed
- Typical range: 512-4096 samples

#### Number of Elements vs. Targets
- Always ensure: num_ant_elements > num_targets
- More elements improve resolution and accuracy
- Minimum: 3 elements for 2D DOA estimation

### Performance Considerations

- **Computational Complexity**: MUSIC O(N³), Root-MUSIC O(N²) where N = array elements
- **Memory Usage**: Correlation matrices require N² complex storage
- **Accuracy**: Improves with SNR, snapshot length, and array aperture
- **Resolution**: Limited by array geometry and algorithm choice

---

## Troubleshooting

### Common Issues

1. **Poor DOA Accuracy**
   - Check array calibration
   - Verify element spacing
   - Increase snapshot size
   - Ensure sufficient SNR

2. **Ambiguous Results**
   - Reduce element spacing
   - Check for spatial aliasing
   - Verify target count parameter

3. **Calibration Problems**
   - Ensure pilot source is at known angle
   - Check phase stability
   - Verify timing synchronization

### Error Messages

- "num_ant_ele must be > num_targets": Increase array elements or reduce target count
- "norm_spacing must be ≤ 0.5": Reduce element spacing or increase frequency
- "overlap_size must be < snapshot_size": Adjust overlap parameter
