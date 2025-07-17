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

class serial_connection(gr.sync_block):
    """
    docstring for block serial_connection
    """
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200, data_format="servo", debug=False, num_inputs=1):
        gr.sync_block.__init__(self,
            name="serial_connection",
            in_sig=[(numpy.float32, num_inputs)],
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
        for value in input_items[0]:  
            if self.data_format == "csv":
                # Convert to CSV format and send
                servo_angle = int(max(0.0, min(180.0, float(value))))

                if self.debug:
                    print("Sending CSV data.")
                csv_data = f"{value}\n"
                self.serial.write(csv_data.encode('utf-8'))
                
            else:
                sys.stderr.write("Unsupported data format\n")
                sys.exit(1)

        return len(input_items[0])
    
    def __del__(self):
        """Clean up serial connection when block is destroyed"""
        if hasattr(self, 'serial') and self.serial.is_open:
            self.serial.close()
            if self.debug:
                print("Serial connection closed.")
