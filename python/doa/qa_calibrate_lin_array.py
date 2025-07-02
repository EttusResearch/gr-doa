#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Ettus Research LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import numpy as np
try:
    from gnuradio.doa import calibrate_lin_array
except ImportError:
    import os
    import sys
    dirname, filename = os.path.split(os.path.abspath(__file__))
    sys.path.append(os.path.join(dirname, "bindings"))
    from gnuradio.doa import calibrate_lin_array

class qa_calibrate_lin_array(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        # Set up parameters
        norm_spacing = 0.5
        num_ant_ele = 4
        pilot_angle = 45.0
        
        # Create a correlation matrix of appropriate size
        # The matrix size must be num_ant_ele x num_ant_ele = 16 complex values
        corr_matrix = np.eye(num_ant_ele, dtype=np.complex64).flatten()
        
        # Create blocks
        src = blocks.vector_source_c(corr_matrix, False, num_ant_ele * num_ant_ele)
        calibrate = calibrate_lin_array(norm_spacing, num_ant_ele, pilot_angle)
        dst = blocks.vector_sink_c(num_ant_ele)
        
        # Connect blocks
        self.tb.connect(src, calibrate)
        self.tb.connect(calibrate, dst)
        
        # Run the flowgraph
        self.tb.run()
        
        # Check results
        # Just a basic check that the block runs without errors
        result = dst.data()
        self.assertEqual(len(result), 1)  # Should get one vector out


if __name__ == '__main__':
    gr_unittest.run(qa_calibrate_lin_array)
