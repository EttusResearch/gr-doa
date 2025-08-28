"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import os
from datetime import datetime


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Triggered 3-Channel Float Recorder with Angle Stepping"""

    def __init__(self, skip_interval=20, samples_to_record=10):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='3-Channel Phase Offset Recorder',   # will show up in GRC
            in_sig=[np.float32, np.float32, np.float32],  # 3 float inputs
            out_sig=[]  # no outputs, this is a sink block
        )
        
        self.angle = 0
        self.folder = "testdata/phase_offsets/calibrated"
        os.makedirs(self.folder, exist_ok=True)
        
        self.recording = False
        self.skip_interval = skip_interval
        self.samples_to_record = samples_to_record
        self.recorded_samples = [[], [], []]  # separate lists for each channel
        self.sample_counter = 0
        
        # Message-Port for Trigger
        self.message_port_register_in(gr.pmt.intern("in"))
        self.set_msg_handler(gr.pmt.intern("in"), self.handle_trigger)

    def handle_trigger(self, msg):
        if not self.recording and self.angle <= 180:
            print(f"[Trigger] Recording started at angle {self.angle}°")
            self.recording = True
            self.recorded_samples = [[], [], []]  # reset all channels
            self.sample_counter = 0

    def work(self, input_items, output_items):
        """Record samples from 3 channels with trigger and angle stepping"""
        if not self.recording:
            return len(input_items[0])
        
        # Get the minimum length across all input channels for this work call
        min_len = min(len(input_items[0]), len(input_items[1]), len(input_items[2]))
        
        for i in range(min_len):
            if self.recording:
                # Only record every skip_interval-th sample using modulo
                if self.sample_counter % self.skip_interval == 0:
                    # Record from all channels simultaneously
                    self.recorded_samples[0].append(float(input_items[0][i]))
                    self.recorded_samples[1].append(float(input_items[1][i]))
                    self.recorded_samples[2].append(float(input_items[2][i]))
                
                self.sample_counter += 1
                
                # Check if we have enough samples
                if len(self.recorded_samples[0]) >= self.samples_to_record:
                    self._save_file()
                    self.recording = False
                    self.angle += 10
                    
                    if self.angle > 180:
                        print("[Recorder] Maximum angle limit reached. Recording stopped.")
                    break  # recording finished for this trigger
        
        return len(input_items[0])
    
    def _save_file(self):
        """Save recorded samples to file"""
        # Safety check: ensure all channels have data
        if not all(len(channel_data) > 0 for channel_data in self.recorded_samples):
            print("[Recorder] Error: Not all channels have data. Skipping save.")
            return
        
        # Use the minimum length to avoid index errors
        min_samples = min(len(channel_data) for channel_data in self.recorded_samples)
        if min_samples == 0:
            print("[Recorder] Error: No samples recorded. Skipping save.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"phase_offset_{self.angle}deg_{timestamp}.dat"
        filepath = os.path.join(self.folder, filename)
        
        with open(filepath, "w") as f:
            f.write(f"# 3-Channel Phase Offset Recording\n")
            f.write(f"# Angle: {self.angle}°\n")
            f.write(f"# Timestamp: {timestamp}\n")
            f.write(f"# Samples per channel: {min_samples}\n")
            f.write(f"# Format: Channel_0, Channel_1, Channel_2\n")
            f.write("#\n")
            
            # Write values row by row using min_samples to avoid index errors
            for i in range(min_samples):
                values = [
                    self.recorded_samples[0][i],
                    self.recorded_samples[1][i], 
                    self.recorded_samples[2][i]
                ]
                f.write(f"{values[0]:.6f}, {values[1]:.6f}, {values[2]:.6f}\n")
        
        print(f"[Recorder] File saved: {filepath} with {min_samples} samples")