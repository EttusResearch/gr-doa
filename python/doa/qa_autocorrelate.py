#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Ettus Research LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import itertools
import oct2py
import numpy
import os
# from gnuradio import blocks
try:
    from gnuradio.doa import autocorrelate
except ImportError:
    import sys
    dirname, filename = os.path.split(os.path.abspath(__file__))
    sys.path.append(os.path.join(dirname, "bindings"))
    from gnuradio.doa import autocorrelate


class qa_autocorrelate(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t (self):
        # length of each snapshot
        len_ss = 2048
        # overlap size of each snapshot
        overlap_size = 512
        # num of inputs
        num_inputs = 4
        # apply Forward-Backward Averaging?
        FB = False

        # Generate auto-correlation vector from octave
        oc = oct2py.Oct2Py()
        qa_tests_path = os.path.join(os.path.dirname(__file__), 'qa_tests')
        oc.addpath(qa_tests_path)
        # Add the parent directory containing the class folder
        oc.addpath(os.path.dirname(qa_tests_path))
        print(oc)
        # Call the octave function to generate the test input
        # The function returns a tuple: (expected_S_x, data)
        result = oc.doa_testbench_create('autocorrelate_test_input_gen', len_ss, overlap_size, num_inputs, FB)
        expected_S_x = result[0]
        data = result[1]
        
        # Convert to a format that can be flattened
        # We need to ensure expected_S_x is iterable
        if isinstance(expected_S_x, numpy.ndarray):
            if expected_S_x.ndim == 0:  # It's a scalar
                expected_S_x = [expected_S_x.item()]
            elif expected_S_x.ndim == 1:  # It's a 1D array
                expected_S_x = expected_S_x.tolist()
            else:  # It's a multi-dimensional array
                expected_S_x = expected_S_x.flatten().tolist()
        
        # num of snapshots
        n_ss = len(expected_S_x)//(num_inputs*num_inputs)

        ##################################################
        # Blocks & Connections
        ##################################################
        self.doa_autocorrelate_0 = autocorrelate(num_inputs, len_ss, overlap_size, FB)
        self.vec_sink = blocks.vector_sink_c(num_inputs*num_inputs)
        
        # Check if data is 1D or 2D
        if isinstance(data, numpy.ndarray) and data.ndim == 1:
            # If data is 1D, reshape it into a 2D array where each column is a copy of the data
            # This is a temporary solution - ideally, we should fix the Octave function to return proper 2D data
            data_len = len(data)
            data_reshaped = numpy.zeros((data_len, num_inputs), dtype=complex)
            for i in range(num_inputs):
                data_reshaped[:, i] = data  # Each column gets a copy of the data
        else:
            data_reshaped = data
            
        # setup sources
        for p in range(num_inputs):
            # Add vector source
            object_name_vs = 'vec_source_'+str(p)
            setattr(self, object_name_vs, blocks.vector_source_c(data_reshaped[:, p].tolist(), False) )
            # Connect
            self.tb.connect((getattr(self,object_name_vs), 0), (self.doa_autocorrelate_0, p))
        
        self.tb.connect((self.doa_autocorrelate_0, 0), (self.vec_sink, 0))

        # set up fg
        self.tb.run ()
        observed_S_x = self.vec_sink.data()

        # check data
        expected_S_x_equals_observed_S_x = True
        for ii in range(n_ss*num_inputs*num_inputs):            
            if abs(expected_S_x[ii]-observed_S_x[ii]) > 1.0:
                expected_S_x_equals_observed_S_x = False

            self.assertTrue(expected_S_x_equals_observed_S_x)

    def test_002_t (self):
        # length of each snapshot
        len_ss = 1024
        # overlap size of each snapshot
        overlap_size = 256
        # num of inputs
        num_inputs = 8
        # apply Forward-Backward Averaging?
        FB = True

        # Generate auto-correlation vector from octave
        oc = oct2py.Oct2Py()
        qa_tests_path = os.path.join(os.path.dirname(__file__), 'qa_tests')
        oc.addpath(qa_tests_path)
        # Add the parent directory containing the class folder
        oc.addpath(os.path.dirname(qa_tests_path))
        result = oc.doa_testbench_create('autocorrelate_test_input_gen', len_ss, overlap_size, num_inputs, FB)
        expected_S_x = result[0]
        data = result[1]
        
        # Convert to a format that can be flattened
        # In Python 3, we need to ensure expected_S_x is iterable
        if isinstance(expected_S_x, numpy.ndarray):
            if expected_S_x.ndim == 0:  # It's a scalar
                expected_S_x = [expected_S_x.item()]
            elif expected_S_x.ndim == 1:  # It's a 1D array
                expected_S_x = expected_S_x.tolist()
            else:  # It's a multi-dimensional array
                expected_S_x = expected_S_x.flatten().tolist()
        
        # num of snapshots
        n_ss = len(expected_S_x)//(num_inputs*num_inputs)

        ##################################################
        # Blocks & Connections
        ##################################################
        self.doa_autocorrelate_0 = autocorrelate(num_inputs, len_ss, overlap_size, FB)
        self.vec_sink = blocks.vector_sink_c(num_inputs*num_inputs)
        
        # Check if data is 1D or 2D
        if isinstance(data, numpy.ndarray) and data.ndim == 1:
            # If data is 1D, reshape it into a 2D array where each column is a copy of the data
            # This is a temporary solution - ideally, we should fix the Octave function to return proper 2D data
            data_len = len(data)
            data_reshaped = numpy.zeros((data_len, num_inputs), dtype=complex)
            for i in range(num_inputs):
                data_reshaped[:, i] = data  # Each column gets a copy of the data
        else:
            data_reshaped = data
            
        # setup sources
        for p in range(num_inputs):
            # Add vector source
            object_name_vs = 'vec_source_'+str(p)
            setattr(self, object_name_vs, blocks.vector_source_c(data_reshaped[:, p].tolist(), False) )
            # Connect
            self.tb.connect((getattr(self,object_name_vs), 0), (self.doa_autocorrelate_0, p))

        self.tb.connect((self.doa_autocorrelate_0, 0), (self.vec_sink, 0))

        # set up fg
        self.tb.run ()
        observed_S_x = self.vec_sink.data()

        # check data
        expected_S_x_equals_observed_S_x = True
        for ii in range(n_ss*num_inputs*num_inputs):            
            if abs(expected_S_x[ii]-observed_S_x[ii]) > 1.0:
                expected_S_x_equals_observed_S_x = False

            self.assertTrue(expected_S_x_equals_observed_S_x)

    def test_003_t (self):
        # length of each snapshot
        len_ss = 256
        # overlap size of each snapshot
        overlap_size = 32
        # num of inputs
        num_inputs = 4
        # apply Forward-Backward Averaging?
        FB = True

        # Generate auto-correlation vector from octave
        oc = oct2py.Oct2Py()
        qa_tests_path = os.path.join(os.path.dirname(__file__), 'qa_tests')
        oc.addpath(qa_tests_path)
        # Add the parent directory containing the class folder
        oc.addpath(os.path.dirname(qa_tests_path))
        result = oc.doa_testbench_create('autocorrelate_test_input_gen', len_ss, overlap_size, num_inputs, FB)
        expected_S_x = result[0]
        data = result[1]
        
        # Convert to a format that can be flattened
        # In Python 3, we need to ensure expected_S_x is iterable
        if isinstance(expected_S_x, numpy.ndarray):
            if expected_S_x.ndim == 0:  # It's a scalar
                expected_S_x = [expected_S_x.item()]
            elif expected_S_x.ndim == 1:  # It's a 1D array
                expected_S_x = expected_S_x.tolist()
            else:  # It's a multi-dimensional array
                expected_S_x = expected_S_x.flatten().tolist()
        
        # num of snapshots
        n_ss = len(expected_S_x)//(num_inputs*num_inputs)

        ##################################################
        # Blocks & Connections
        ##################################################
        self.doa_autocorrelate_0 = autocorrelate(num_inputs, len_ss, overlap_size, FB)
        self.vec_sink = blocks.vector_sink_c(num_inputs*num_inputs)
        
        # Check if data is 1D or 2D
        if isinstance(data, numpy.ndarray) and data.ndim == 1:
            # If data is 1D, reshape it into a 2D array where each column is a copy of the data
            # This is a temporary solution - ideally, we should fix the Octave function to return proper 2D data
            data_len = len(data)
            data_reshaped = numpy.zeros((data_len, num_inputs), dtype=complex)
            for i in range(num_inputs):
                data_reshaped[:, i] = data  # Each column gets a copy of the data
        else:
            data_reshaped = data
            
        # setup sources
        for p in range(num_inputs):
            # Add vector source
            object_name_vs = 'vec_source_'+str(p)
            setattr(self, object_name_vs, blocks.vector_source_c(data_reshaped[:, p].tolist(), False) )
            # Connect
            self.tb.connect((getattr(self,object_name_vs), 0), (self.doa_autocorrelate_0, p))

        self.tb.connect((self.doa_autocorrelate_0, 0), (self.vec_sink, 0))

        # set up fg
        self.tb.run ()
        observed_S_x = self.vec_sink.data()

        # check data
        expected_S_x_equals_observed_S_x = True
        for ii in range(n_ss*num_inputs*num_inputs):            
            if abs(expected_S_x[ii]-observed_S_x[ii]) > 1.0:
                expected_S_x_equals_observed_S_x = False

            self.assertTrue(expected_S_x_equals_observed_S_x)

if __name__ == '__main__':
    gr_unittest.run(qa_autocorrelate)
