#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Ettus Research LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
import sys


def gen_sig_io(num_elements,sig_type):
    # Dynamically create types for signature
    io = []
    for i in range(num_elements):
        io.append(sig_type)
    return io


class average_and_save(gr.sync_block):
    """
    average_and_save: This block will average 'samples_to_average' samples from
    each input, write those average(s) to 'config_file' and terminate.  This block
    is primarily used in DoA to provide configuration files for phase correction
    blocks.
    """

    def __init__(self, samples_to_average, num_inputs, config_filename):
        gr.sync_block.__init__(self,
            name="average_and_save",
            in_sig=gen_sig_io(num_inputs, numpy.float32),
            out_sig=None)

        # Make sure we get enough inputs
        self.set_output_multiple(samples_to_average)

        # Save parameters
        self.config_filename = config_filename
        self.num_inputs = num_inputs
        self.samples_to_average = samples_to_average
        # Check file
        try:
            file = open(self.config_filename, 'w') # clear it out
            file.close()
        except:
            sys.stderr.write("Configuration "+config_filename+", not writable\n")
            print(sys.stderr)
            sys.exit(1)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        # Open file
        file = open(self.config_filename, 'w')
        for i in range(self.num_inputs):
            # Average samples
            average = numpy.mean(input_items[i][:self.samples_to_average])
            # print average
            # Write to config
            if file.write(str(average)+"\n") != None:
                sys.stderr.write("Writing file failed\n")
                print(sys.stderr)
                sys.exit(1)

        file.close()
        # Stop flowgraph
        return -1
