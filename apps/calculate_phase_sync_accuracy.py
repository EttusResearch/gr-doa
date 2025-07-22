#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: calculate_phase_sync_accuracy
# Author: jreitmei
# GNU Radio version: v3.11.0.0git-979-g1055cd27

def struct(data): return type('Struct', (object,), data)()
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




class calculate_phase_sync_accuracy(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "calculate_phase_sync_accuracy", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.input_variables = input_variables = struct({

            'SampleRate': 1e6,

            'ToneFreq': 10e3,

            'CenterFreq': 462e6,

            'NumArrayElements': 4,

            'Gain': 60,

            'RxAddr': "addr=10.88.136.40",

            'DirectoryConfigFiles': "/tmp",

            'RelativePhaseOffsets': "measure_relative_phase_offsets_446.cfg",

            'CorrectedPhaseOffsets': "measure_corrected_phase_offsets_446.cfg",

            'SkipAhead': 2**13,

            'Samples2FindMax': 2**11,









        })
        self.samp_rate = samp_rate = 32000
        self.rel_phase_offsets_file_name = rel_phase_offsets_file_name = os.path.join(input_variables.DirectoryConfigFiles, input_variables.RelativePhaseOffsets)
        self.corrected_phase_offsets_file_name = corrected_phase_offsets_file_name = os.path.join(input_variables.DirectoryConfigFiles, input_variables.CorrectedPhaseOffsets)

        ##################################################
        # Blocks
        ##################################################

        self.doa_x440_usrp_source_0 = doa.x440_usrp_source(samp_rate=input_variables.SampleRate, center_freq=input_variables.CenterFreq, gain=input_variables.Gain, sources=input_variables.NumArrayElements, addresses=input_variables.RxAddr, device_args='master_clock_rate=200e6')
        self.doa_phase_offset_est_0 = doa.phase_offset_est(input_variables.NumArrayElements, input_variables.SkipAhead)
        self.doa_phase_correct_hier_0 = doa.phase_correct_hier(num_ports=input_variables.NumArrayElements, config_filename=rel_phase_offsets_file_name)
        self.doa_findmax_and_save_0 = doa.findmax_and_save(input_variables.Samples2FindMax, (input_variables.NumArrayElements-1), corrected_phase_offsets_file_name)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.doa_phase_correct_hier_0, 1), (self.doa_phase_offset_est_0, 1))
        self.connect((self.doa_phase_correct_hier_0, 3), (self.doa_phase_offset_est_0, 3))
        self.connect((self.doa_phase_correct_hier_0, 0), (self.doa_phase_offset_est_0, 0))
        self.connect((self.doa_phase_correct_hier_0, 2), (self.doa_phase_offset_est_0, 2))
        self.connect((self.doa_phase_offset_est_0, 0), (self.doa_findmax_and_save_0, 0))
        self.connect((self.doa_phase_offset_est_0, 2), (self.doa_findmax_and_save_0, 2))
        self.connect((self.doa_phase_offset_est_0, 1), (self.doa_findmax_and_save_0, 1))
        self.connect((self.doa_x440_usrp_source_0, 0), (self.doa_phase_correct_hier_0, 0))
        self.connect((self.doa_x440_usrp_source_0, 3), (self.doa_phase_correct_hier_0, 3))
        self.connect((self.doa_x440_usrp_source_0, 2), (self.doa_phase_correct_hier_0, 2))
        self.connect((self.doa_x440_usrp_source_0, 1), (self.doa_phase_correct_hier_0, 1))


    def get_input_variables(self):
        return self.input_variables

    def set_input_variables(self, input_variables):
        self.input_variables = input_variables

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rel_phase_offsets_file_name(self):
        return self.rel_phase_offsets_file_name

    def set_rel_phase_offsets_file_name(self, rel_phase_offsets_file_name):
        self.rel_phase_offsets_file_name = rel_phase_offsets_file_name

    def get_corrected_phase_offsets_file_name(self):
        return self.corrected_phase_offsets_file_name

    def set_corrected_phase_offsets_file_name(self, corrected_phase_offsets_file_name):
        self.corrected_phase_offsets_file_name = corrected_phase_offsets_file_name




def main(top_block_cls=calculate_phase_sync_accuracy, options=None):
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
