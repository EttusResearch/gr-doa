#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: run_MUSIC_lin_array
# Author: jreitmei
# GNU Radio version: v3.11.0.0git-979-g1055cd27

from PyQt5 import Qt
from gnuradio import qtgui
def struct(data): return type('Struct', (object,), data)()
from PyQt5 import QtCore
from gnuradio import blocks
from gnuradio import doa
import gnuradio.doa as doa
import numpy
import sip
import threading
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation




class run_MUSIC_lin_array_simulation(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "run_MUSIC_lin_array", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("run_MUSIC_lin_array")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "run_MUSIC_lin_array_simulation")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.theta1_deg = theta1_deg = 123
        self.theta0_deg = theta0_deg = 30
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

            'NumTargets': 1,

            'PSpectrumLength': 2**10,

            'DirectoryConfigFiles': "/tmp",

            'RelativePhaseOffsets': "measure_relative_phase_offsets_245.cfg",







        })
        self.theta1 = theta1 = numpy.pi*theta1_deg/180
        self.theta0 = theta0 = numpy.pi*theta0_deg/180
        self.ant_locs = ant_locs = numpy.dot(input_variables.NormSpacing, numpy.arange(input_variables.NumArrayElements/2, -input_variables.NumArrayElements/2, -1) if (input_variables.NumArrayElements%2==1) else numpy.arange(input_variables.NumArrayElements/2-0.5, -input_variables.NumArrayElements/2-0.5, -1))
        self.amv1 = amv1 = numpy.exp(-1j*ant_locs*2*numpy.pi*numpy.cos(theta1))
        self.amv0 = amv0 = numpy.exp(-1j*ant_locs*2*numpy.pi*numpy.cos(theta0))
        self.array_manifold_matrix = array_manifold_matrix = numpy.array([amv0, amv1]).transpose()

        ##################################################
        # Blocks
        ##################################################

        self._theta1_deg_range = qtgui.Range(0, 180, 1, 123, 200)
        self._theta1_deg_win = qtgui.RangeWidget(self._theta1_deg_range, self.set_theta1_deg, "AoA", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._theta1_deg_win)
        self._theta0_deg_range = qtgui.Range(0, 180, 1, 30, 200)
        self._theta0_deg_win = qtgui.RangeWidget(self._theta0_deg_range, self.set_theta0_deg, "AoA", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._theta0_deg_win)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            input_variables.PSpectrumLength,
            0,
            (180.0/input_variables.PSpectrumLength),
            "angle (in degrees)",
            "Pseudo-Spectrum (dB)",
            "",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.05)
        self.qtgui_vector_sink_f_0.set_y_axis((-50), 0)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(True)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.qtgui_number_sink_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            input_variables.NumTargets,
            None # parent
        )
        self.qtgui_number_sink_1.set_update_time(0.10)
        self.qtgui_number_sink_1.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(input_variables.NumTargets):
            self.qtgui_number_sink_1.set_min(i, 0)
            self.qtgui_number_sink_1.set_max(i, 180)
            self.qtgui_number_sink_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_1.set_label(i, labels[i])
            self.qtgui_number_sink_1.set_unit(i, units[i])
            self.qtgui_number_sink_1.set_factor(i, factor[i])

        self.qtgui_number_sink_1.enable_autoscale(False)
        self._qtgui_number_sink_1_win = sip.wrapinstance(self.qtgui_number_sink_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_1_win)
        self.doa_x440_usrp_source_0 = doa.x440_usrp_source(samp_rate=input_variables.SampleRate, center_freq=input_variables.CenterFreq, gain=input_variables.Gain, sources=input_variables.NumArrayElements, addresses=input_variables.RxAddr, device_args='master_clock_rate=200e6')
        self.doa_phase_correct_hier_0 = doa.phase_correct_hier(num_ports=input_variables.NumArrayElements, config_filename='rel_phase_offsets_file_name')
        self.doa_find_local_max_0 = doa.find_local_max(input_variables.NumTargets, input_variables.PSpectrumLength, 0.0, 180.0)
        self.doa_autocorrelate_0 = doa.autocorrelate(input_variables.NumArrayElements, input_variables.SnapshotSize, input_variables.OverlapSize, 0)
        self.doa_MUSIC_lin_array_0 = doa.MUSIC_lin_array(input_variables.NormSpacing, input_variables.NumTargets, input_variables.NumArrayElements, input_variables.PSpectrumLength)
        self.blocks_vector_to_streams_0 = blocks.vector_to_streams(gr.sizeof_float*1, input_variables.NumTargets)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*input_variables.NumTargets)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_to_streams_0, 0), (self.qtgui_number_sink_1, 0))
        self.connect((self.doa_MUSIC_lin_array_0, 0), (self.doa_find_local_max_0, 0))
        self.connect((self.doa_MUSIC_lin_array_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.doa_autocorrelate_0, 0), (self.doa_MUSIC_lin_array_0, 0))
        self.connect((self.doa_find_local_max_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.doa_find_local_max_0, 1), (self.blocks_vector_to_streams_0, 0))
        self.connect((self.doa_phase_correct_hier_0, 1), (self.doa_autocorrelate_0, 1))
        self.connect((self.doa_phase_correct_hier_0, 2), (self.doa_autocorrelate_0, 2))
        self.connect((self.doa_phase_correct_hier_0, 3), (self.doa_autocorrelate_0, 3))
        self.connect((self.doa_phase_correct_hier_0, 0), (self.doa_autocorrelate_0, 0))
        self.connect((self.doa_x440_usrp_source_0, 1), (self.doa_phase_correct_hier_0, 1))
        self.connect((self.doa_x440_usrp_source_0, 2), (self.doa_phase_correct_hier_0, 2))
        self.connect((self.doa_x440_usrp_source_0, 0), (self.doa_phase_correct_hier_0, 0))
        self.connect((self.doa_x440_usrp_source_0, 3), (self.doa_phase_correct_hier_0, 3))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "run_MUSIC_lin_array_simulation")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_theta1_deg(self):
        return self.theta1_deg

    def set_theta1_deg(self, theta1_deg):
        self.theta1_deg = theta1_deg
        self.set_theta1(numpy.pi*self.theta1_deg/180)

    def get_theta0_deg(self):
        return self.theta0_deg

    def set_theta0_deg(self, theta0_deg):
        self.theta0_deg = theta0_deg
        self.set_theta0(numpy.pi*self.theta0_deg/180)

    def get_input_variables(self):
        return self.input_variables

    def set_input_variables(self, input_variables):
        self.input_variables = input_variables

    def get_theta1(self):
        return self.theta1

    def set_theta1(self, theta1):
        self.theta1 = theta1
        self.set_amv1(numpy.exp(-1j*self.ant_locs*2*numpy.pi*numpy.cos(self.theta1)))

    def get_theta0(self):
        return self.theta0

    def set_theta0(self, theta0):
        self.theta0 = theta0
        self.set_amv0(numpy.exp(-1j*self.ant_locs*2*numpy.pi*numpy.cos(self.theta0)))

    def get_ant_locs(self):
        return self.ant_locs

    def set_ant_locs(self, ant_locs):
        self.ant_locs = ant_locs
        self.set_amv0(numpy.exp(-1j*self.ant_locs*2*numpy.pi*numpy.cos(self.theta0)))
        self.set_amv1(numpy.exp(-1j*self.ant_locs*2*numpy.pi*numpy.cos(self.theta1)))

    def get_amv1(self):
        return self.amv1

    def set_amv1(self, amv1):
        self.amv1 = amv1
        self.set_array_manifold_matrix(numpy.array([self.amv0, self.amv1]).transpose())

    def get_amv0(self):
        return self.amv0

    def set_amv0(self, amv0):
        self.amv0 = amv0
        self.set_array_manifold_matrix(numpy.array([self.amv0, self.amv1]).transpose())

    def get_array_manifold_matrix(self):
        return self.array_manifold_matrix

    def set_array_manifold_matrix(self, array_manifold_matrix):
        self.array_manifold_matrix = array_manifold_matrix




def main(top_block_cls=run_MUSIC_lin_array_simulation, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
