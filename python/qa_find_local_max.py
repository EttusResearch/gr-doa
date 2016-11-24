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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import doa_swig as doa
import oct2py
import numpy
import os
from subprocess import Popen, PIPE

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
		oc.addpath(os.path.dirname(__file__))	
		data, expected_pks, expected_t_pks = oc.test001_findpeaks(self.num_max_vals, self.vector_len)
		data = data.flatten().tolist()

		##################################################
		# Blocks
		##################################################
		self.blocks_vector_source_x_0 = blocks.vector_source_f(data, False, self.vector_len, [])
		self.doa_find_local_max_0 = doa.find_local_max(self.num_max_vals, self.vector_len, 0.0, 2*numpy.pi)
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
			self.assertAlmostEqual(expected_pks[i], measured_pks[i], 5) and self.assertAlmostEqual(expected_t_pks[i], measured_t_pks[i], 5)

	def test_002_t (self):
		self.vector_len = 2**12
		self.num_max_vals = 5

		# generate vector from octave
		oc = oct2py.Oct2Py()
		oc.addpath(os.path.dirname(__file__))
		data, expected_pks, expected_t_pks = oc.test002_findpeaks(self.num_max_vals, self.vector_len)
		data = data.flatten().tolist()

		##################################################
		# Blocks
		##################################################
		self.blocks_vector_source_x_0 = blocks.vector_source_f(data, False, self.vector_len, [])
		self.doa_find_local_max_0 = doa.find_local_max(self.num_max_vals, self.vector_len, 0.0, 2*numpy.pi)
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
			self.assertAlmostEqual(expected_pks[i], measured_pks[i], 5) and self.assertAlmostEqual(expected_t_pks[i], measured_t_pks[i], 5)

if __name__ == '__main__':
	gr_unittest.run(qa_find_local_max, "qa_find_local_max.xml")
