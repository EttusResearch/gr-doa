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
    def __init__(self, port="/dev/ttyACM0", baudrate=115200, debug=False, dimensions=1, low_hysteresis=3.0, high_hysteresis=18.0, mirror=False, stability_window_size=20, stability_threshold=2.0, force_update_threshold=10.0):
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
        self.low_hysteresis = low_hysteresis  # Lower threshold for hysteresis band
        self.high_hysteresis = high_hysteresis  # Upper threshold for hysteresis band
        self.mirror = mirror  # Mirror input angles (180° - input)
        
        # Store last sent angles for each servo to implement hysteresis
        self.last_angles = [None] * dimensions
        # Store last actual angles (for sending old value when hysteresis not met)
        self.last_actual_angles = [None] * dimensions
        # Track if this is the first value for each servo (skip first value)
        self.first_value_received = [False] * dimensions
        
        # Stability detection parameters
        self.stability_window_size = stability_window_size  # Number of recent values to track
        self.stability_threshold = 2.0   # Max variation in degrees to consider "stable"
        self.force_update_threshold = 10.0  # Min difference to trigger forced update
        
        # Sliding window buffers for each servo to track recent values
        self.value_buffers = [[] for _ in range(dimensions)]

        if self.debug:
            print(f"Serial connection established on {port} at {baudrate} baud.")
            print(f"Configured for {dimensions} servo(s)")
            print(f"Hysteresis band: {low_hysteresis}° - {high_hysteresis}°")
            print(f"Changes will only be sent if angle difference is between {low_hysteresis}° and {high_hysteresis}°")
            print(f"Mirror mode: {'enabled' if mirror else 'disabled'}")

    # check stability of recent values for error correction
    def _is_value_stable(self, servo_idx, current_value):
        """Check if recent values are stable (low variation)"""
        buffer = self.value_buffers[servo_idx]
        
        if len(buffer) < self.stability_window_size:
            return False
        
        # Calculate variation in recent values
        values = list(buffer)
        min_val = min(values)
        max_val = max(values)
        variation = max_val - min_val
        
        return variation <= self.stability_threshold

    # New method to determine if we should force update
    def _should_force_update(self, servo_idx, current_value):
        """Check if we should force update due to large difference from stable values"""
        if self.last_angles[servo_idx] is None:
            return False
        
        # Check if values are stable
        if not self._is_value_stable(servo_idx, current_value):
            return False
        
        # Check if there's a significant difference between stable value and last sent angle
        stable_average = sum(self.value_buffers[servo_idx]) / len(self.value_buffers[servo_idx])
        difference = abs(stable_average - self.last_angles[servo_idx])
        
        return difference >= self.force_update_threshold

    def _print_debug_info(self, data, servo_idx, servo_angle, angle_to_send, force_update=False):
        """Print debug information about servo commands"""
        if force_update:
            print(f"Sent: {data.strip()} (FORCED UPDATE)")
        elif angle_to_send == servo_angle:
            if self.last_angles[servo_idx] is not None:
                angle_diff = abs(servo_angle - self.last_angles[servo_idx])
                print(f"Sent: {data.strip()} (new angle, diff: {angle_diff:.1f}°)")
            else:
                print(f"Sent: {data.strip()} (first angle)")
        else:
            current_diff = abs(servo_angle - self.last_angles[servo_idx])
            print(f"Sent: {data.strip()} (old angle - diff {current_diff:.1f}° outside {self.low_hysteresis}°-{self.high_hysteresis}° band)")

    # Main processing method 
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
                    
                    # Apply mirror transformation if enabled
                    if self.mirror:
                        value = 180.0 - value
                    
                    # Skip the first value for each servo
                    if not self.first_value_received[servo_idx]:
                        self.first_value_received[servo_idx] = True
                        if self.debug:
                            print(f"Skipping first value for servo {servo_letters[servo_idx]}: {value}")
                        continue
                    
                    # Convert to servo angle (0-180 degrees)
                    servo_angle = int(max(0.0, min(180.0, float(value))))
                    
                    # Update sliding window buffer
                    buffer = self.value_buffers[servo_idx]
                    buffer.append(servo_angle)
                    if len(buffer) > self.stability_window_size:
                        buffer.pop(0)  # Remove oldest value
                    
                    # Store the current actual angle
                    self.last_actual_angles[servo_idx] = servo_angle
                    
                    # Implement hysteresis band logic with forced update check
                    angle_to_send = servo_angle  # Default to current angle
                    force_update = False
                    
                    if self.last_angles[servo_idx] is None:
                        # First time - always send current angle
                        angle_to_send = servo_angle
                    else:
                        # Check if we should force update due to stable values being far from servo position
                        if self._should_force_update(servo_idx, servo_angle):
                            angle_to_send = servo_angle
                            force_update = True
                            if self.debug:
                                stable_avg = sum(self.value_buffers[servo_idx]) / len(self.value_buffers[servo_idx])
                                print(f"Servo {servo_letters[servo_idx]}: Forcing update - stable at {stable_avg:.1f}°, servo at {self.last_angles[servo_idx]}°")
                        else:
                            # Normal hysteresis logic
                            angle_diff = abs(servo_angle - self.last_angles[servo_idx])
                            
                            # Hysteresis band: only send new angle if change is between low_hysteresis and high_hysteresis
                            if self.low_hysteresis <= angle_diff <= self.high_hysteresis:
                                angle_to_send = servo_angle
                            else:
                                # Outside hysteresis band - send old value (last sent angle)
                                angle_to_send = self.last_angles[servo_idx]
                    
                    # Always send something (either new or old angle)
                    servo_letter = servo_letters[servo_idx]
                    
                    # Format: A_90, B_120, C_150
                    data = f"{servo_letter}_{angle_to_send}\n"
                    
                    # Send to serial port
                    self.serial.write(data.encode('utf-8'))
                    
                    # Update last sent angle only if we sent a new angle (not old value)
                    if angle_to_send == servo_angle:
                        self.last_angles[servo_idx] = servo_angle
                    
                    # Debug output for the command line
                    if self.debug:
                        self._print_debug_info(data, servo_idx, servo_angle, angle_to_send, force_update)
                    
                    # Small delay between servo commands to avoid overwhelming micro:bit
                    time.sleep(0.01)
                        
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
