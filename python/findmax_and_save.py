#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 
# Srikanth Pagadarai<srikanth.pagadarai@gmail.com>
# Travis Collins<travisfcollins@gmail.com>.				
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import sys
import doa_swig as doa

def gen_sig_io(num_elements,sig_type):
    # Dynamically create types for signature
    io = []
    for i in range(num_elements):
        io.append(sig_type)
    return io

class findmax_and_save(gr.sync_block):
    """
    This block will find the max. value of the first 'samples_to_findmax' samples from each input, write those max value(s) to a 'config_file' and terminate.  
    """
    def __init__(self, samples_to_findmax, num_inputs, config_filename):
        gr.sync_block.__init__(self,
            name="findmax_and_save",
            in_sig=gen_sig_io(num_inputs, numpy.float32),
            out_sig=None)

        # Make sure we get enough inputs
        self.set_output_multiple(samples_to_findmax)

        # Save parameters
        self.config_filename = config_filename
        self.num_inputs = num_inputs
        self.samples_to_findmax = samples_to_findmax
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
            # Find max. of samples
            max = numpy.amax(input_items[i][:self.samples_to_findmax])
            # print max
            # Write to config
            if file.write(str(max)+"\n") != None:
                sys.stderr.write("Writing file failed\n")
                print(sys.stderr)
                sys.exit(1)

        file.close()
        # Stop flowgraph
        return -1
