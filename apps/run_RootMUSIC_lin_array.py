#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: run_RootMUSIC_lin_array
# Author: jreitmei
# GNU Radio version: v3.11.0.0git-979-g1055cd27

from PyQt5 import Qt
from gnuradio import qtgui
def struct(data): return type('Struct', (object,), data)()
from gnuradio import doa
import gnuradio.doa as doa
import os
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




class run_RootMUSIC_lin_array(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "run_RootMUSIC_lin_array", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("run_RootMUSIC_lin_array")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "run_RootMUSIC_lin_array")

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
        self.input_variables = input_variables = struct({

            'ToneFreq': 10000,

            'SampleRate': 1e6,

            'CenterFreq': 462e6,

            'RxAddr': "addr=10.88.136.14",

            'Gain': 60,

            'NumArrayElements': 4,

            'NormSpacing': 0.5,

            'SnapshotSize': 2**11,

            'OverlapSize': 2**9,

            'NumTargets': 1,

            'PSpectrumLength': 2**10,









        })

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_number_sink_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
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

        for i in range(1):
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
        self.qtgui_compass_0 = self._qtgui_compass_0_win = qtgui.GrCompass('', 250, 0.10, False, 1,False,1,"default")
        self._qtgui_compass_0_win.setColors("default","red", "black", "black")
        self._qtgui_compass_0 = self._qtgui_compass_0_win
        self.top_layout.addWidget(self._qtgui_compass_0_win)
        self.doa_x440_usrp_source_0 = doa.x440_usrp_source(samp_rate=input_variables.SampleRate, center_freq=input_variables.CenterFreq, gain=input_variables.Gain, sources=input_variables.NumArrayElements, addresses=input_variables.RxAddr, device_args='master_clock_rate=200e6')
        self.doa_rootMUSIC_linear_array_0 = doa.rootMUSIC_linear_array(input_variables.NormSpacing, input_variables.NumTargets, 4)
        self.doa_phase_correct_hier_0 = doa.phase_correct_hier(num_ports=input_variables.NumArrayElements, config_filename='/tmp/measure_relative_phase_offsets_446.cfg')
        self.doa_autocorrelate_0 = doa.autocorrelate(input_variables.NumArrayElements, input_variables.SnapshotSize, input_variables.OverlapSize, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.doa_autocorrelate_0, 0), (self.doa_rootMUSIC_linear_array_0, 0))
        self.connect((self.doa_phase_correct_hier_0, 3), (self.doa_autocorrelate_0, 3))
        self.connect((self.doa_phase_correct_hier_0, 2), (self.doa_autocorrelate_0, 2))
        self.connect((self.doa_phase_correct_hier_0, 1), (self.doa_autocorrelate_0, 1))
        self.connect((self.doa_phase_correct_hier_0, 0), (self.doa_autocorrelate_0, 0))
        self.connect((self.doa_rootMUSIC_linear_array_0, 0), (self.qtgui_compass_0, 0))
        self.connect((self.doa_rootMUSIC_linear_array_0, 0), (self.qtgui_number_sink_1, 0))
        self.connect((self.doa_x440_usrp_source_0, 0), (self.doa_phase_correct_hier_0, 0))
        self.connect((self.doa_x440_usrp_source_0, 1), (self.doa_phase_correct_hier_0, 1))
        self.connect((self.doa_x440_usrp_source_0, 3), (self.doa_phase_correct_hier_0, 3))
        self.connect((self.doa_x440_usrp_source_0, 2), (self.doa_phase_correct_hier_0, 2))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "run_RootMUSIC_lin_array")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_input_variables(self):
        return self.input_variables

    def set_input_variables(self, input_variables):
        self.input_variables = input_variables




def main(top_block_cls=run_RootMUSIC_lin_array, options=None):

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
