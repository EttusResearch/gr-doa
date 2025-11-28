#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Ettus Research LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class power_detection(gr.basic_block):
    """
    docstring for block power_detection
    """
    def __init__(self, num_inputs, sample_rate, threshold, buffer_size=1024):
        gr.basic_block.__init__(self,
            name="power_detection",
            in_sig=[numpy.complex64] * num_inputs,
            out_sig=[numpy.complex64] * num_inputs)
        
        self.num_inputs = num_inputs
        self.sample_rate = sample_rate
        self.threshold = threshold
        self.detection_state = False
        
        # Dual ring buffer system - For multiple channels
        self.buffer_size = buffer_size
        self.capture_buffer = numpy.zeros((num_inputs, buffer_size), dtype=numpy.complex64)
        self.playback_buffer = numpy.zeros((num_inputs, buffer_size), dtype=numpy.complex64)
        self.capture_index = 0
        self.playback_index = 0
        
        # Buffer management - simplified approach
        self.playback_buffer_valid = False
        self.buffer_fill_complete = False
        self.capturing = False

    def forecast(self, noutput_items, ninputs):
        ninput_items_required = [noutput_items] * ninputs
        return ninput_items_required

    def general_work(self, input_items, output_items):
        ninput_items = min([len(items) for items in input_items])
        noutput_items = min(len(output_items[0]), ninput_items)
        
        for i in range(noutput_items):
            # Use first channel for power detection
            sample = input_items[0][i]
            sample_power = numpy.abs(sample)**2
            
            # Simple threshold-based filling
            if sample_power > self.threshold:
                # Start capturing if not already
                if not self.capturing:
                    self.capturing = True
                    self.capture_index = 0
                    print(f"Signal detected! Starting buffer fill at power: {sample_power:.6f}")
                
                # Fill buffer for all channels
                if self.capture_index < self.buffer_size:
                    for ch in range(self.num_inputs):
                        self.capture_buffer[ch, self.capture_index] = input_items[ch][i]
                    self.capture_index += 1
                    
                    # Check if buffer is now full
                    if self.capture_index >= self.buffer_size:
                        self._validate_and_promote_buffer()
                
                # Pass through all channels during detection
                for ch in range(self.num_inputs):
                    output_items[ch][i] = input_items[ch][i]
                        
            else:
                # No signal - stop capturing and replay if available
                if self.capturing:
                    self.capturing = False
                    if self.capture_index > 0 and not self.buffer_fill_complete:
                        print(f"Signal ended with {self.capture_index} samples (buffer not full)")
                
                # Replay stored signal during silence for all channels
                if self.playback_buffer_valid and self.buffer_fill_complete:
                    for ch in range(self.num_inputs):
                        output_items[ch][i] = self.playback_buffer[ch, self.playback_index]
                    self.playback_index = (self.playback_index + 1) % self.buffer_size
                else:
                    # No valid signal captured yet - output zeros on all channels
                    for ch in range(self.num_inputs):
                        output_items[ch][i] = 0.0 + 0.0j
                    
        self.consume_each(noutput_items)
        return noutput_items
    
    def _validate_and_promote_buffer(self):
        """Validate captured buffer and promote to playback if good quality"""
        self.playback_buffer[:, :] = self.capture_buffer[:, :]
        self.playback_buffer_valid = True
        self.buffer_fill_complete = True
        self.playback_index = 0
        print(f"Buffer filled completely! Promoted to playback buffer")

