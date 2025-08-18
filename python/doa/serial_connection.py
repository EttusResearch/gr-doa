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
    def __init__(self, port="/dev/ttyACM0", baudrate=115200, debug=False, dimensions=1, hysteresis=3.0):
        # Create input signature with separate channels for each servo
        in_sig = [numpy.float32] * dimensions  # dimensions separate float32 input channels
        
        gr.sync_block.__init__(self,
            name="serial_connection",
            in_sig=in_sig,
            out_sig=None)

        # Check file
        try:
            self.serial = serial.Serial(port, baudrate, timeout=1)
        except Exception as e:
            sys.stderr.write(f"Serial port configuration error: {e}\n")
            sys.exit(1)

        self.debug = debug
        self.dimensions = dimensions  # Number of servos (1 dimension = 1 servo)
        self.hysteresis = hysteresis  # Hysteresis threshold in degrees
        
        # Store last sent angles for each servo to implement hysteresis
        self.last_angles = [None] * dimensions

        if self.debug:
            print(f"Serial connection established on {port} at {baudrate} baud.")
            print(f"Configured for {dimensions} servo(s)")
            print(f"Hysteresis threshold: {hysteresis} degrees")

    def work(self, input_items, output_items):
        # input_items is now a list with one array per input channel
        # input_items[0] = samples from channel 0 (servo A)
        # input_items[1] = samples from channel 1 (servo B) if dimensions >= 2
        # input_items[2] = samples from channel 2 (servo C) if dimensions >= 3
        
        num_samples = len(input_items[0])  # All channels have the same number of samples
        
        for sample_idx in range(num_samples):
            try:
                # Map servo indices to letters: 0=A, 1=B, 2=C
                servo_letters = ['A', 'B', 'C']
                
                # Process each input channel (servo)
                for servo_idx in range(self.dimensions):
                    if servo_idx >= len(servo_letters):
                        break  # Skip if more than 3 servos
                    
                    # Get the value from the corresponding input channel
                    value = input_items[servo_idx][sample_idx]
                    
                    # Convert to servo angle (0-180 degrees)
                    servo_angle = int(max(0.0, min(180.0, float(value))))
                    
                    # Implement hysteresis: only send command if angle change exceeds threshold
                    should_send = False
                    if self.last_angles[servo_idx] is None:
                        # First time - always send
                        should_send = True
                    else:
                        # Check if change exceeds hysteresis threshold
                        angle_diff = abs(servo_angle - self.last_angles[servo_idx])
                        if angle_diff >= self.hysteresis:
                            should_send = True
                    
                    if should_send:
                        servo_letter = servo_letters[servo_idx]
                        
                        # Format: A_90, B_120, C_150
                        data = f"{servo_letter}_{servo_angle}\n"
                        
                        # Send to serial port
                        self.serial.write(data.encode('utf-8'))
                        
                        # Update last sent angle
                        self.last_angles[servo_idx] = servo_angle
                        
                        if self.debug:
                            print(f"Sent: {data.strip()}")
                        
                        # Small delay between servo commands to avoid overwhelming micro:bit
                        time.sleep(0.01)
                    elif self.debug:
                        print(f"Servo {servo_letters[servo_idx]}: Angle change {abs(servo_angle - self.last_angles[servo_idx]):.1f}° < {self.hysteresis}° threshold, not sending")
                        
            except (ValueError, TypeError) as e:
                if self.debug:
                    print(f"Error converting values at sample {sample_idx}: {e}")
                continue

        return num_samples
    
    def __del__(self):
        """Clean up serial connection when block is destroyed"""
        # Close serial connection
        if hasattr(self, 'serial') and self.serial.is_open:
            self.serial.close()
            if hasattr(self, 'debug') and self.debug:
                print("Serial connection closed.")
