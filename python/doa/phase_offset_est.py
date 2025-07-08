#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Ettus Research LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import pmt
# Remove direct import of doa as it's within the gnuradio.doa module already

def gen_sig_io(num_elements,sig_type):
    # Dynamically create types for signature
    io = []
    for i in range(num_elements):
        io.append(sig_type*1)
    return io

class phase_offset_est(gr.hier_block2):
    """
    This block estimates the repeatable phase offset at the output of a USRP X310 equipped with two TwinRXs. The output is a value in [0, 2*pi).
    """
    def __init__(self, num_ports=2, n_skip_ahead=8192):
        gr.hier_block2.__init__(
            self, "phase_offset_est",
             gr.io_signaturev(num_ports, num_ports, gen_sig_io(num_ports,gr.sizeof_gr_complex)),
            gr.io_signaturev(num_ports-1, num_ports-1, gen_sig_io(num_ports-1,gr.sizeof_float)),
        ) 

        ##################################################
        # Parameters
        ##################################################
        self.n_skip_ahead = n_skip_ahead
        self.num_ports = num_ports

        # Create skip head blocks and connect them to the inputs
        self.skiphead = []
        for p in range(0, num_ports):
            object_name_skiphead = 'blocks_skiphead_'+str(p)
            self.skiphead.append(blocks.skiphead(gr.sizeof_gr_complex*1, n_skip_ahead))
            self.connect((self, p), (self.skiphead[p], 0))

        #Create blocks computing subtracted phases and connect the results to the outputs
        self.multiply_conjugate = []
        self.complex_to_arg = []
        for p in range(0, num_ports-1):
            self.multiply_conjugate.append(blocks.multiply_conjugate_cc(1))
            self.complex_to_arg.append(blocks.complex_to_arg(1))

            self.connect((self.skiphead[0], 0), (self.multiply_conjugate[p], 0))
            self.connect((self.skiphead[p+1], 0), (self.multiply_conjugate[p], 1))
            self.connect((self.multiply_conjugate[p], 0), (self.complex_to_arg[p], 0))
            self.connect((self.complex_to_arg[p], 0), (self, p))
