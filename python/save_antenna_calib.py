#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016
# Srikanth Pagadarai <srikanth.pagadarai@gmail.com>
# Travis F. Collins <travisfcollins@gmail.com>
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
import numpy
from itertools import chain

class save_antenna_calib(gr.sync_block):
    """
    save_antenna_calib: Save antenna calibration values to configuration file,
    which will be used in the 'Antenna Correction' block.
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
            # Write to file
            if file.write(str(GainEst)+' '+str(PhaseEst)+"\n") != None:
                sys.stderr.write("Writing file failed\n")
                print(sys.stderr)
                sys.exit(1)

        file.close()
        return -1# Stop flowgraph
