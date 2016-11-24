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

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import pmt
import doa

def gen_sig_io(num_elements,sig_type):
    # Dynamically create types for signature
    io = []
    for i in range(num_elements):
        io.append(sig_type*1)
    return io

class twinrx_phase_offset_est(gr.hier_block2):
    """
    This block estimates the repeatable phase offset at the output of a USRP X310 equipped with two TwinRXs. The output is a value in [0, 2*pi). 
    """
    def __init__(self, num_ports=2, n_skip_ahead=8192):
        gr.hier_block2.__init__(
            self, "TwinRx Phase Offset Estimate",
            gr.io_signaturev(num_ports, num_ports, gen_sig_io(num_ports,gr.sizeof_gr_complex)),
            gr.io_signaturev(num_ports-1, num_ports-1, gen_sig_io(num_ports-1,gr.sizeof_float)),
        )

        ##################################################
        # Parameters
        ##################################################
        self.n_skip_ahead = n_skip_ahead
        self.num_ports = num_ports

	##################################################
	# Reference Connection
	##################################################
	# Blocks
	self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, n_skip_ahead)
	self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)

	# Connections 
	self.connect((self, 0), (self.blocks_skiphead_0, 0))
	self.connect((self.blocks_skiphead_0, 0), (self.blocks_complex_to_arg_0, 0))        

	##################################################
	# All Other Connections
	##################################################
	for p in range(1, num_ports):
		##################
		# Blocks 
		##################

		# Skip Ahead Block
		object_name_skiphead = 'blocks_skiphead_'+str(p)
		setattr(self, object_name_skiphead, blocks.skiphead(gr.sizeof_gr_complex*1, n_skip_ahead))

		# Complex-to-Arg Block
		object_name_complex_to_arg = 'blocks_complex_to_arg_'+str(p)
		setattr(self, object_name_complex_to_arg, blocks.complex_to_arg(1))

		# Subtract Block
		object_name_sub = 'blocks_sub_ff_'+str(p)
		setattr(self, object_name_sub, blocks.sub_ff(1))
		

		##################
		# Connections
		##################

		self.connect((self, p), (getattr(self,object_name_skiphead), 0))
		self.connect((getattr(self,object_name_skiphead), 0), (getattr(self,object_name_complex_to_arg), 0))
		self.connect((getattr(self,object_name_complex_to_arg), 0), (getattr(self,object_name_sub), 1))
		self.connect((self.blocks_complex_to_arg_0, 0), (getattr(self,object_name_sub), 0))
		self.connect((getattr(self,object_name_sub), 0), (self, p-1))
