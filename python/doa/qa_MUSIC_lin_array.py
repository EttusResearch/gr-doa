#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Ettus Research LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import scipy
import oct2py
import os

try:
    from gnuradio.doa import MUSIC_lin_array
    from gnuradio.doa import find_local_max
except ImportError:
    import sys
    dirname, filename = os.path.split(os.path.abspath(__file__))
    sys.path.append(os.path.join(dirname, "bindings"))
    from gnuradio.doa import MUSIC_lin_array
    from gnuradio.doa import find_local_max


class qa_MUSIC_lin_array (gr_unittest.TestCase):

    ##################################################
    # Variables
    ##################################################

    def setUp(self):
        self.tb = gr.top_block()
        self.samp_rate = 32000
        self.pspectrum_len = 1024
        

    def tearDown(self):
        self.tb = None

    def test_001_MUSIC_aoa23(self):
        # length of each snapshot
        len_ss = 256
        # overlap size of each snapshot
        overlap_size = 32
        # apply Forward-Backward Averaging?
        FB = True
        # normalized_spacing
        norm_spacing = 0.4
        # number of sources 
        num_srcs = 1
        # expected angle-of-arrival
        expected_aoa = 23.0
        # number of array elements
        num_arr_ele = 8
        # simulate perturbation?
        PERTURB = False

        # Generate auto-correlation vector from octave
        oc = oct2py.Oct2Py()
        qa_tests_path = os.path.join(os.path.dirname(__file__), 'qa_tests')
        oc.addpath(qa_tests_path)
        # Add the parent directory containing the class folder
        oc.addpath(os.path.dirname(qa_tests_path))
        music_linear_input = oc.doa_testbench_create('music_test_input_gen', len_ss, overlap_size, num_arr_ele, FB, 'linear', num_arr_ele, norm_spacing, PERTURB, expected_aoa)
        music_linear_input = music_linear_input.flatten().tolist()

        ##################################################
        # Blocks
        ##################################################
        self.doa_MUSIC_0 = MUSIC_lin_array(norm_spacing, num_srcs, num_arr_ele, self.pspectrum_len)
        self.doa_find_local_max_0 = find_local_max(num_srcs, self.pspectrum_len, 0.0, 180.0)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*num_srcs)
        self.vec_sink = blocks.vector_sink_f(num_srcs)
        self.vec_source = blocks.vector_source_c(music_linear_input, False, num_arr_ele * num_arr_ele)

        ##################################################
        # Connections
        ##################################################
        self.tb.connect((self.vec_source, 0), (self.doa_MUSIC_0, 0))
        self.tb.connect((self.doa_MUSIC_0, 0), (self.doa_find_local_max_0, 0))    
        self.tb.connect((self.doa_find_local_max_0, 1), (self.vec_sink, 0))
        self.tb.connect((self.doa_find_local_max_0, 0), (self.blocks_null_sink_0, 0))

        # set up fg
        self.tb.run()

        # get data from sink
        aoa_output_23 = self.vec_sink.data()

        # check
        measured_aoa_is_23 = True
        for i in range(len(aoa_output_23)):            
            if (abs(aoa_output_23[i] - expected_aoa) > 2.0):
                measured_aoa_is_23 = False

        self.assertTrue(measured_aoa_is_23)

    
    def test_002_MUSIC_aoa121(self):
        # length of each snapshot
        len_ss = 256
        # overlap size of each snapshot
        overlap_size = 32
        # apply Forward-Backward Averaging?
        FB = True
        # normalized_spacing
        norm_spacing = 0.5
        # number of sources 
        num_srcs = 1
        # expected angle-of-arrival
        expected_aoa = 121.0
        # number of array elements
        num_arr_ele = 16
        # simulate perturbation?
        PERTURB = False

        # Generate auto-correlation vector from octave
        oc = oct2py.Oct2Py()
        qa_tests_path = os.path.join(os.path.dirname(__file__), 'qa_tests')
        oc.addpath(qa_tests_path)
        # Add the parent directory containing the class folder
        oc.addpath(os.path.dirname(qa_tests_path))
        music_linear_input = oc.doa_testbench_create('music_test_input_gen', len_ss, overlap_size, num_arr_ele, FB, 'linear', num_arr_ele, norm_spacing, PERTURB, expected_aoa)
        music_linear_input = music_linear_input.flatten().tolist()

        ##################################################
        # Blocks
        ##################################################
        self.doa_MUSIC_0 = MUSIC_lin_array(norm_spacing, num_srcs, num_arr_ele, self.pspectrum_len)
        self.doa_find_local_max_0 = find_local_max(num_srcs, self.pspectrum_len, 0.0, 180.0)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*num_srcs)
        self.vec_sink = blocks.vector_sink_f(num_srcs)
        self.vec_source = blocks.vector_source_c(music_linear_input, False, num_arr_ele * num_arr_ele)

        ##################################################
        # Connections
        ##################################################
        self.tb.connect((self.vec_source, 0), (self.doa_MUSIC_0, 0))
        self.tb.connect((self.doa_MUSIC_0, 0), (self.doa_find_local_max_0, 0))    
        self.tb.connect((self.doa_find_local_max_0, 1), (self.vec_sink, 0))
        self.tb.connect((self.doa_find_local_max_0, 0), (self.blocks_null_sink_0, 0))

        # set up fg
        self.tb.run()

        # get data from sink
        aoa_output_121 = self.vec_sink.data()

        # check
        measured_aoa_is_121 = True
        for i in range(len(aoa_output_121)):
            if (abs(aoa_output_121[i] - expected_aoa) > 2.0):
                measured_aoa_is_121 = False

        self.assertTrue(measured_aoa_is_121) 


if __name__ == '__main__':
    gr_unittest.run(qa_MUSIC_lin_array)
