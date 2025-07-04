#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Ettus Research LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
import sys
from itertools import chain
from gnuradio import gr

class save_antenna_calib(gr.sync_block):
    """
    This block saves the antenna gain and phase values estimated by an antenna calibration block in a config-file. 
    The values stored are averaged over a certain number of samples.
    """
    def __init__(self, num_inputs, config_filename="", samples_to_average=1024):
        gr.sync_block.__init__(self,
            name="save_antenna_calib",
            in_sig=[(numpy.float32,num_inputs),(numpy.float32,num_inputs)],
            out_sig=None)

        self.num_inputs = num_inputs
        self.config_filename = config_filename
        self.samples_to_average = samples_to_average

        # Make sure we get enough inputs
        self.set_output_multiple(samples_to_average)

        # Check file
        try:
            file = open(self.config_filename, 'w') # Clear file
            file.close()
        except:
            sys.stderr.write("Configuration "+config_filename+", not valid\n")
            print(sys.stderr)
            sys.exit(1)



    def work(self, input_items, output_items):

        # Open file
        file = open(self.config_filename, 'w')

        for i in range(self.num_inputs):
            # Average across all estimates
            G = list(chain.from_iterable(input_items[0]))
            GainEst = numpy.mean(G[i::self.num_inputs])
            P = list(chain.from_iterable(input_items[1]))
            PhaseEst = numpy.mean(P[i::self.num_inputs])
                        
            # Print values to console
            print(f"Antenna {i}: Gain = {GainEst}, Phase = {PhaseEst}")
            
            # Write to file
            try:
                file.write(f"{GainEst} {PhaseEst}\n")
            except IOError:
                sys.stderr.write("Writing file failed\n")
                print(sys.stderr)
                sys.exit(1)

        file.close()
        return -1  # Stop flowgraph