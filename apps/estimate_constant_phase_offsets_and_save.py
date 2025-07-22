#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: estimate_constant_phase_offsets_and_save
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




class estimate_constant_phase_offsets_and_save(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "estimate_constant_phase_offsets_and_save", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("estimate_constant_phase_offsets_and_save")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "estimate_constant_phase_offsets_and_save")

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

            'SampleRate': 1e6,

            'ToneFreq': 12.5e3,

            'CenterFreq': 462e6,

            'Gain': 60,

            'NumArrayElements': 4,

            'RxAddr': "addr=10.88.136.40",

            'DirectoryConfigFiles': "/tmp",

            'RelativePhaseOffsets': "measure_relative_phase_offsets_446.cfg",

            'SkipAhead': 2**13,

            'Samples2FindMax': 2**11,










        })
        self.rel_phase_offsets_file_name = rel_phase_offsets_file_name = os.path.join(input_variables.DirectoryConfigFiles, input_variables.RelativePhaseOffsets)
        self.multConst = multConst = 2

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024 , #size
            input_variables.SampleRate, #samp_rate
            "", #name
            4, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1 - Real', 'Signal 2', 'Signal 3 - Real', 'Signal 4', 'Signal 5 - Real',
            'Signal 6', 'Signal 7 - Real', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['black', 'red', 'black', 'black', 'black',
            'magenta', 'black', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 0, 1, 0, 1,
            0, 1, 0, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(8):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.doa_x440_usrp_source_0 = doa.x440_usrp_source(samp_rate=input_variables.SampleRate, center_freq=input_variables.CenterFreq, gain=input_variables.Gain, sources=input_variables.NumArrayElements, addresses=input_variables.RxAddr, device_args='master_clock_rate=200e6')
        self.doa_phase_offset_est_0 = doa.phase_offset_est(input_variables.NumArrayElements, input_variables.SkipAhead)
        self.doa_findmax_and_save_0 = doa.findmax_and_save(input_variables.Samples2FindMax, (input_variables.NumArrayElements-1), rel_phase_offsets_file_name)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.doa_phase_offset_est_0, 1), (self.doa_findmax_and_save_0, 1))
        self.connect((self.doa_phase_offset_est_0, 2), (self.doa_findmax_and_save_0, 2))
        self.connect((self.doa_phase_offset_est_0, 0), (self.doa_findmax_and_save_0, 0))
        self.connect((self.doa_x440_usrp_source_0, 0), (self.doa_phase_offset_est_0, 0))
        self.connect((self.doa_x440_usrp_source_0, 1), (self.doa_phase_offset_est_0, 1))
        self.connect((self.doa_x440_usrp_source_0, 2), (self.doa_phase_offset_est_0, 2))
        self.connect((self.doa_x440_usrp_source_0, 3), (self.doa_phase_offset_est_0, 3))
        self.connect((self.doa_x440_usrp_source_0, 3), (self.qtgui_time_sink_x_0, 3))
        self.connect((self.doa_x440_usrp_source_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.doa_x440_usrp_source_0, 2), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.doa_x440_usrp_source_0, 1), (self.qtgui_time_sink_x_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "estimate_constant_phase_offsets_and_save")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_input_variables(self):
        return self.input_variables

    def set_input_variables(self, input_variables):
        self.input_variables = input_variables

    def get_rel_phase_offsets_file_name(self):
        return self.rel_phase_offsets_file_name

    def set_rel_phase_offsets_file_name(self, rel_phase_offsets_file_name):
        self.rel_phase_offsets_file_name = rel_phase_offsets_file_name

    def get_multConst(self):
        return self.multConst

    def set_multConst(self, multConst):
        self.multConst = multConst




def main(top_block_cls=estimate_constant_phase_offsets_and_save, options=None):

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
