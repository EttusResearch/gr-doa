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
import itertools
import oct2py
import numpy
import os

class qa_calibrate_lin_array (gr_unittest.TestCase):

	def setUp (self):
		self.tb = gr.top_block ()

	def tearDown (self):
		self.tb = None

	def test_001_t (self):	       
		# normalized_spacing
		norm_spacing = 0.3
		# pilot angle
		pilot_doa = 30.0
		# number of antenna array elements
		num_ant_ele = 4
		# length of each snapshot
		len_ss = 2048
		# overlap size of each snapshot
		overlap_size = 512
		# apply Forward-Backward Averaging?
		FB = False
		# simulate perturbation?
		PERTURB = True

		# Generate auto-correlation vector from octave
		oc = oct2py.Oct2Py()
		oc.addpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'examples'))
		S_x, S_x_uncalibrated, ant_pert_vec = oc.doa_testbench_create('music_test_input_gen', len_ss, overlap_size, num_ant_ele, FB, 'linear', num_ant_ele, norm_spacing, PERTURB, pilot_doa)
		S_x_uncalibrated = S_x_uncalibrated.flatten().tolist()
		ant_pert_vec = list(itertools.chain.from_iterable(ant_pert_vec))

		##################################################
		# Blocks
		##################################################
		self.vec_source = blocks.vector_source_c(S_x_uncalibrated, False, num_ant_ele*num_ant_ele)
		self.doa_calibrate_lin_array_0 = doa.calibrate_lin_array(norm_spacing, num_ant_ele, pilot_doa)
		self.vec_sink = blocks.vector_sink_c(num_ant_ele)        

		##################################################
		# Connections
		##################################################
		self.tb.connect((self.vec_source, 0), (self.doa_calibrate_lin_array_0, 0))
		self.tb.connect((self.doa_calibrate_lin_array_0, 0), (self.vec_sink, 0))  

		# set up fg
		self.tb.run ()

		# get data from sink
		ant_pert_vec_est = self.vec_sink.data()
		ant_pert_vec_est = numpy.asarray(ant_pert_vec_est, 'F')
		# num of snapshots
		n_ss = len(ant_pert_vec_est)/num_ant_ele

		# check data
		ant_ele_range = range(0, num_ant_ele)
		expected_result = numpy.zeros(num_ant_ele-1)+1j*numpy.zeros(num_ant_ele-1)
		for ii in range(0, n_ss):
			# calibrated_antenna_resp will contain elements that are all equal
			calibrated_antenna_resp = numpy.divide(ant_pert_vec, ant_pert_vec_est[ii*num_ant_ele+numpy.array(ant_ele_range)])
			self.assertComplexTuplesAlmostEqual(expected_result, numpy.diff(calibrated_antenna_resp), 1)

	def test_002_t (self):	       
		# normalized_spacing
		norm_spacing = 0.5
		# pilot angle
		pilot_doa = 60.0
		# number of antenna array elements
		num_ant_ele = 8
		# num of snapshots
		n_ss = 1000
		# length of each snapshot
		len_ss = 1024
		# overlap size of each snapshot
		overlap_size = 128
		# apply Forward-Backward Averaging?
		FB = True
		# simulate perturbation?
		PERTURB = True

		# Generate auto-correlation vector from octave
		oc = oct2py.Oct2Py()
		oc.addpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'examples'))
		S_x, S_x_uncalibrated, ant_pert_vec = oc.doa_testbench_create('music_test_input_gen', len_ss, overlap_size, num_ant_ele, FB, 'linear', num_ant_ele, norm_spacing, PERTURB, pilot_doa)
		S_x_uncalibrated = S_x_uncalibrated.flatten().tolist()
		ant_pert_vec = list(itertools.chain.from_iterable(ant_pert_vec))

		##################################################
		# Blocks
		##################################################
		self.vec_source = blocks.vector_source_c(S_x_uncalibrated, False, num_ant_ele*num_ant_ele)
		self.doa_calibrate_lin_array_0 = doa.calibrate_lin_array(norm_spacing, num_ant_ele, pilot_doa)
		self.vec_sink = blocks.vector_sink_c(num_ant_ele)        

		##################################################
		# Connections
		##################################################
		self.tb.connect((self.vec_source, 0), (self.doa_calibrate_lin_array_0, 0))
		self.tb.connect((self.doa_calibrate_lin_array_0, 0), (self.vec_sink, 0))  

		# set up fg
		self.tb.run ()

		# get data from sink
		ant_pert_vec_est = self.vec_sink.data()
		ant_pert_vec_est = numpy.asarray(ant_pert_vec_est, 'F')
		# num of snapshots
		n_ss = len(ant_pert_vec_est)/num_ant_ele

		# check data
		ant_ele_range = range(0, num_ant_ele)
		expected_result = numpy.zeros(num_ant_ele-1)+1j*numpy.zeros(num_ant_ele-1)
		for ii in range(0, n_ss):
			# calibrated_antenna_resp will contain elements that are all equal
			calibrated_antenna_resp = numpy.divide(ant_pert_vec, ant_pert_vec_est[ii*num_ant_ele+numpy.array(ant_ele_range)])
			self.assertComplexTuplesAlmostEqual(expected_result, numpy.diff(calibrated_antenna_resp), 1)

	def test_003_t (self):	       
		# normalized_spacing
		norm_spacing = 0.2
		# pilot angle
		pilot_doa = 25.0
		# number of antenna array elements
		num_ant_ele = 4
		# num of snapshots
		n_ss = 800
		# length of each snapshot
		len_ss = 256
		# overlap size of each snapshot
		overlap_size = 64
		# apply Forward-Backward Averaging?
		FB = False
		# simulate perturbation?
		PERTURB = True

		# Generate auto-correlation vector from octave
		oc = oct2py.Oct2Py()
		oc.addpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'examples'))
		S_x, S_x_uncalibrated, ant_pert_vec = oc.doa_testbench_create('music_test_input_gen', len_ss, overlap_size, num_ant_ele, FB, 'linear', num_ant_ele, norm_spacing, PERTURB, pilot_doa)
		S_x_uncalibrated = S_x_uncalibrated.flatten().tolist()
		ant_pert_vec = list(itertools.chain.from_iterable(ant_pert_vec))

		##################################################
		# Blocks
		##################################################
		self.vec_source = blocks.vector_source_c(S_x_uncalibrated, False, num_ant_ele*num_ant_ele)
		self.doa_calibrate_lin_array_0 = doa.calibrate_lin_array(norm_spacing, num_ant_ele, pilot_doa)
		self.vec_sink = blocks.vector_sink_c(num_ant_ele)        

		##################################################
		# Connections
		##################################################
		self.tb.connect((self.vec_source, 0), (self.doa_calibrate_lin_array_0, 0))
		self.tb.connect((self.doa_calibrate_lin_array_0, 0), (self.vec_sink, 0))  

		# set up fg
		self.tb.run ()

		# get data from sink
		ant_pert_vec_est = self.vec_sink.data()
		ant_pert_vec_est = numpy.asarray(ant_pert_vec_est, 'F')
		# num of snapshots
		n_ss = len(ant_pert_vec_est)/num_ant_ele

		# check data
		ant_ele_range = range(0, num_ant_ele)
		expected_result = numpy.zeros(num_ant_ele-1)+1j*numpy.zeros(num_ant_ele-1)
		for ii in range(0, n_ss):
			# calibrated_antenna_resp will contain elements that are all equal
			calibrated_antenna_resp = numpy.divide(ant_pert_vec, ant_pert_vec_est[ii*num_ant_ele+numpy.array(ant_ele_range)])
			self.assertComplexTuplesAlmostEqual(expected_result, numpy.diff(calibrated_antenna_resp), 1)
 
if __name__ == '__main__':
    gr_unittest.run(qa_calibrate_lin_array, "qa_calibrate_lin_array.xml")
