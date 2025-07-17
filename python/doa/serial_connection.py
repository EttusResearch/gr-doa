#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Ettus Research LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
import sys
from gnuradio import gr
import serial
import time

class serial_connection(gr.sync_block):
    """
    docstring for block serial_connection
    """
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200, data_format="csv", debug=False, num_max=1):
        gr.sync_block.__init__(self,
            name="serial_connection",
            in_sig=[(numpy.float32, num_max)],
            out_sig=None)

        # Check file
        try:
            self.serial = serial.Serial(port, baudrate, timeout=1)
        except Exception as e:
            sys.stderr.write(f"Serial port configuration error: {e}\n")
            sys.exit(1)

        self.data_format = data_format
        self.debug = debug

        if self.debug:
            print(f"Serial connection established on {port} at {baudrate} baud.")

        

    def work(self, input_items, output_items):
        # Convert input data to the specified format for servo control
        # Process all samples (each sample is a vector of num_max elements)
        num_samples = len(input_items[0])
        
        for sample_idx in range(num_samples):
            # Transfer via CSV
            if self.data_format == "csv":
                try:
                    # Get the vector for this sample (contains num_max values)
                    vector_values = input_items[0][sample_idx]  # This is a numpy array of length num_max
                    all_values = [float(val) for val in vector_values]
                    
                    # Convert all values to servo angles
                    servo_angles = [int(max(0.0, min(180.0, val))) for val in all_values]
                    
                    if self.debug:
                        print(f"Sending CSV data: original_values={all_values}, servo_angles={servo_angles}")
                    
                    # Real CSV format: num_servo,value1,value2,...,angle1,angle2,...
                    num_servo = "num_servo" + str(len(all_values))
                    # Values as floats
                    values_str = ','.join([f"{val:.3f}" for val in all_values])
                    # Angles as integers
                    angles_str = ','.join([str(angle) for angle in servo_angles])
                    # CSV format
                    csv_data = f"{num_servo},{values_str},{angles_str}\n"
                    # Send the CSV data to the serial port
                    self.serial.write(csv_data.encode('utf-8'))
                    
                except (ValueError, TypeError) as e:
                    if self.debug:
                        print(f"Error converting values at sample {sample_idx}: {e}")
                    continue
                    
            else:
                sys.stderr.write(f"Unsupported data format: {self.data_format}\n")
                sys.exit(1)

        return num_samples
    
    def __del__(self):
        """Clean up serial connection when block is destroyed"""
        if hasattr(self, 'serial') and self.serial.is_open:
            self.serial.close()
            if self.debug:
                print("Serial connection closed.")
