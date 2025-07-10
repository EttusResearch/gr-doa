#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Ettus Research LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import oct2py
import numpy
import os
from subprocess import Popen, PIPE
# from gnuradio import blocks
try:
    from gnuradio.doa import find_local_max
except ImportError:
    import sys
    dirname, filename = os.path.split(os.path.abspath(__file__))
    sys.path.append(os.path.join(dirname, "bindings"))
    from gnuradio.doa import find_local_max

class qa_find_local_max (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()	

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        self.vector_len = 2**11
        self.num_max_vals = 3

        # generate vector from octave
        oc = oct2py.Oct2Py()
        qa_tests_path = os.path.join(os.path.dirname(__file__), 'qa_tests')
        oc.addpath(qa_tests_path)
        # Add the parent directory containing the class folder
        oc.addpath(os.path.dirname(qa_tests_path))
        result = oc.test001_findpeaks(self.num_max_vals, self.vector_len, nout=3)
        data, expected_pks, expected_t_pks = result
        data = data.flatten().tolist()

        ##################################################
        # Blocks
        ##################################################
        self.blocks_vector_source_x_0 = blocks.vector_source_f(data, False, self.vector_len, [])
        self.doa_find_local_max_0 = find_local_max(self.num_max_vals, self.vector_len, 0.0, 2*numpy.pi)
        self.blocks_vector_sink_x_0 = blocks.vector_sink_f(self.num_max_vals)
        self.blocks_vector_sink_x_1 = blocks.vector_sink_f(self.num_max_vals)       

        ##################################################
        # Connections
        ##################################################
        self.tb.connect((self.blocks_vector_source_x_0, 0), (self.doa_find_local_max_0, 0))    
        self.tb.connect((self.doa_find_local_max_0, 0), (self.blocks_vector_sink_x_0, 0))    
        self.tb.connect((self.doa_find_local_max_0, 1), (self.blocks_vector_sink_x_1, 0))  

        # set up fg
        self.tb.run ()

        # get data from sink
        measured_pks = self.blocks_vector_sink_x_0.data()  
        measured_pks_locs = self.blocks_vector_sink_x_1.data()  

        # check data
        for i in range(len(measured_pks)):
            # Convert NumPy array elements to Python floats using item() to extract a single value
            self.assertAlmostEqual(float(expected_pks[i].item()), float(measured_pks[i]), places=5)
            # Use fewer decimal places for location comparison due to floating-point precision differences
            self.assertAlmostEqual(float(expected_t_pks[i].item()), float(measured_pks_locs[i]), places=2)

    def test_002_t (self):
        self.vector_len = 2**12
        self.num_max_vals = 5

        # generate vector from octave
        oc = oct2py.Oct2Py()
        qa_tests_path = os.path.join(os.path.dirname(__file__), 'qa_tests')
        oc.addpath(qa_tests_path)
        # Add the parent directory containing the class folder
        oc.addpath(os.path.dirname(qa_tests_path))
        result = oc.test002_findpeaks(self.num_max_vals, self.vector_len, nout=3)
        data, expected_pks, expected_t_pks = result
        data = data.flatten().tolist()

        ##################################################
        # Blocks
        ##################################################
        self.blocks_vector_source_x_0 = blocks.vector_source_f(data, False, self.vector_len, [])
        self.doa_find_local_max_0 = find_local_max(self.num_max_vals, self.vector_len, 0.0, 2*numpy.pi)
        self.blocks_vector_sink_x_0 = blocks.vector_sink_f(self.num_max_vals)
        self.blocks_vector_sink_x_1 = blocks.vector_sink_f(self.num_max_vals)       

        ##################################################
        # Connections
        ##################################################
        self.tb.connect((self.blocks_vector_source_x_0, 0), (self.doa_find_local_max_0, 0))    
        self.tb.connect((self.doa_find_local_max_0, 0), (self.blocks_vector_sink_x_0, 0))    
        self.tb.connect((self.doa_find_local_max_0, 1), (self.blocks_vector_sink_x_1, 0))  

        # set up fg
        self.tb.run ()

        # get data from sink
        measured_pks = self.blocks_vector_sink_x_0.data()  
        measured_pks_locs = self.blocks_vector_sink_x_1.data()  	

        # compare the two functions
        for i in range(len(measured_pks)):
            # Convert NumPy array elements to Python floats
            self.assertAlmostEqual(float(expected_pks[i].item()), float(measured_pks[i]), places=5)
            # Use fewer decimal places for location comparison due to floating-point precision differences
            self.assertAlmostEqual(float(expected_t_pks[i].item()), float(measured_pks_locs[i]), places=2)

if __name__ == '__main__':
    gr_unittest.run(qa_find_local_max)
