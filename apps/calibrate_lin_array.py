#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: jreitmei
# GNU Radio version: v3.11.0.0git-979-g1055cd27

def struct(data): return type('Struct', (object,), data)()
from gnuradio import blocks
from gnuradio import doa
import gnuradio.doa as doa
import os
import threading
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation




class calibrate_lin_array(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.input_variables = input_variables = struct({

            'ToneFreq': 10e3,

            'SampleRate': 1e6,

            'CenterFreq': 462e6,

            'RxAddr': "addr=10.88.136.34",

            'Gain': 60,

            'NumArrayElements': 4,

            'NormSpacing': 0.5,

            'SnapshotSize': 2**11,

            'OverlapSize': 2**9,

            'PilotAngle': 45.0,

            'DirectoryConfigFiles': "/tmp",

            'RelativePhaseOffsets': "measure_relative_phase_offsets_446.cfg",

            'AntennaCalibration': "calibration_lin_array_446.cfg",

            'Samples2Avg': 2**11,






        })
        self.rel_phase_offsets_file_name = rel_phase_offsets_file_name = os.path.join(input_variables.DirectoryConfigFiles, input_variables.RelativePhaseOffsets)
        self.antenna_calibration_file_name = antenna_calibration_file_name = os.path.join(input_variables.DirectoryConfigFiles, input_variables.AntennaCalibration)

        ##################################################
        # Blocks
        ##################################################

        self.doa_x440_usrp_source_0 = doa.x440_usrp_source(samp_rate=input_variables.SampleRate, center_freq=input_variables.CenterFreq, gain=input_variables.Gain, sources=input_variables.NumArrayElements, addresses=input_variables.RxAddr, device_args='master_clock_rate=200e6')
        self.doa_save_antenna_calib_0 = doa.save_antenna_calib(input_variables.NumArrayElements, antenna_calibration_file_name, input_variables.Samples2Avg)
        self.doa_phase_correct_hier_0 = doa.phase_correct_hier(num_ports=input_variables.NumArrayElements, config_filename=rel_phase_offsets_file_name)
        self.doa_calibrate_lin_array_0 = doa.calibrate_lin_array(input_variables.NormSpacing, input_variables.NumArrayElements, input_variables.PilotAngle)
        self.doa_autocorrelate_0 = doa.autocorrelate(input_variables.NumArrayElements, input_variables.SnapshotSize, input_variables.OverlapSize, 0)
        self.blocks_complex_to_magphase_0 = blocks.complex_to_magphase(input_variables.NumArrayElements)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_magphase_0, 0), (self.doa_save_antenna_calib_0, 0))
        self.connect((self.blocks_complex_to_magphase_0, 1), (self.doa_save_antenna_calib_0, 1))
        self.connect((self.doa_autocorrelate_0, 0), (self.doa_calibrate_lin_array_0, 0))
        self.connect((self.doa_calibrate_lin_array_0, 0), (self.blocks_complex_to_magphase_0, 0))
        self.connect((self.doa_phase_correct_hier_0, 0), (self.doa_autocorrelate_0, 0))
        self.connect((self.doa_phase_correct_hier_0, 3), (self.doa_autocorrelate_0, 3))
        self.connect((self.doa_phase_correct_hier_0, 2), (self.doa_autocorrelate_0, 2))
        self.connect((self.doa_phase_correct_hier_0, 1), (self.doa_autocorrelate_0, 1))
        self.connect((self.doa_x440_usrp_source_0, 1), (self.doa_phase_correct_hier_0, 1))
        self.connect((self.doa_x440_usrp_source_0, 2), (self.doa_phase_correct_hier_0, 2))
        self.connect((self.doa_x440_usrp_source_0, 0), (self.doa_phase_correct_hier_0, 0))
        self.connect((self.doa_x440_usrp_source_0, 3), (self.doa_phase_correct_hier_0, 3))


    def get_input_variables(self):
        return self.input_variables

    def set_input_variables(self, input_variables):
        self.input_variables = input_variables

    def get_rel_phase_offsets_file_name(self):
        return self.rel_phase_offsets_file_name

    def set_rel_phase_offsets_file_name(self, rel_phase_offsets_file_name):
        self.rel_phase_offsets_file_name = rel_phase_offsets_file_name

    def get_antenna_calibration_file_name(self):
        return self.antenna_calibration_file_name

    def set_antenna_calibration_file_name(self, antenna_calibration_file_name):
        self.antenna_calibration_file_name = antenna_calibration_file_name




def main(top_block_cls=calibrate_lin_array, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
