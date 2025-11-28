#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Ettus Research LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
import os
from gnuradio import gr

class signal_replay(gr.sync_block):
    """
    Signal replay block that loads and continuously outputs a signal from file.
    
    This block reads a numpy array file containing complex signal data and 
    outputs it continuously. It supports optional interpolation and repetition.
    """
    def __init__(self, filename="predefined singal/20MHz_5_4_oversampling_05msframe_45mssilent.npy", repeat=True, interpolation=1):
        gr.sync_block.__init__(self,
            name="signal_replay",
            in_sig=None,  # No inputs (source block)
            out_sig=[np.complex64])  # Complex output
        
        # If using relative path, make it relative to the gr-doa root directory
        if not os.path.isabs(filename):
            # Get the directory containing this Python file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Navigate up to the gr-doa root directory (from python/doa/ to root)
            gr_doa_root = os.path.dirname(os.path.dirname(current_dir))
            filename = os.path.join(gr_doa_root, filename)
        
        # Store configuration parameters
        self.filename = filename                        # Path to the signal file (.npy format)
        self.repeat = repeat                            # Whether to loop the signal continuously
        self.interpolation = interpolation              # Factor to repeat each sample (up/down sampling)
        self.position = 0                               # Current position in the interpolated output stream
        
        # Load and validate signal data from file
        try:
            # Load numpy array from file (expected format: complex64 or convertible)
            self.signal_data = np.load(filename)
            
            # Ensure data is in the correct complex64 format for GNU Radio
            if self.signal_data.dtype != np.complex64:
                self.signal_data = self.signal_data.astype(np.complex64)
                
            gr.log.info(f"Successfully loaded signal file: {filename}")
            gr.log.info(f"Signal length: {len(self.signal_data)} samples")
            
        except Exception as e:
            # Fallback to single zero sample if file loading fails
            gr.log.error(f"Failed to load signal file {filename}: {e}")
            gr.log.error(f"Make sure the file exists and is a valid numpy array")
            self.signal_data = np.array([0], dtype=np.complex64)

    def work(self, input_items, output_items):
        """
        Main processing function called by GNU Radio scheduler.
        
        This function fills the output buffer with signal samples, applying
        interpolation and handling repetition/end-of-file conditions.
        
        Args:
            input_items: Input buffers (unused, this is a source block)
            output_items: List containing the output buffer to fill
            
        Returns:
            Number of output items produced
        """

        out = output_items[0]                # Get the output buffer
        noutput_items = len(out)            # Number of samples requested
        
        # Fill output buffer sample by sample
        for i in range(noutput_items):
            # Check if we've reached the end of the signal
            if self.position >= len(self.signal_data) * self.interpolation:
                if self.repeat:
                    # Reset to beginning for continuous playback
                    self.position = 0
                else:
                    # Fill remaining samples with zeros and indicate end
                    out[i:] = 0
                    return i
            
            # Calculate which original sample to use (accounting for interpolation)
            sample_idx = self.position // self.interpolation
            
            # Output the sample (with bounds checking)
            if sample_idx < len(self.signal_data):
                out[i] = self.signal_data[sample_idx]
            else:
                out[i] = 0
                
            # Advance position in the interpolated stream
            self.position += 1
            
        return noutput_items  # Return number of samples actually produced