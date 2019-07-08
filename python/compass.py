#!/usr/bin/env python
#
# Copyright 2016
# Travis F. Collins <travisfcollins@gmail.com>
# Srikanth Pagadarai <srikanth.pagadarai@gmail.com>
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
import numpy
from gnuradio import gr;
import time
import random

from PyQt4 import Qt, QtCore, QtGui
import PyQt4.Qwt5 as Qwt

class compass(gr.sync_block, Qwt.QwtPlot):
    __pyqtSignals__ = ("updatePlot(int)")

    def __init__(self, label="", min_val=-90, max_val=90, step=10, arc_bias=0, needle_N=1, *args):
        gr.sync_block.__init__(self,name="QT Compass",in_sig=[numpy.float32]*needle_N,out_sig=[])
        Qwt.QwtPlot.__init__(self, *args)

        # Set parameters
        self.update_period = 0.1
        self.last = time.time()
        self.next_angles = []

        ### QT STUFF

        # Setup overall layouts
        self.this_layout = Qt.QVBoxLayout()
        self.compass_layout = Qt.QGridLayout()

        # Setup Dials
        self.dial_list = []
        for i in range(needle_N):
            dial = Qwt.QwtDial(self)
            dial_palette = dial.palette()
            transparent_color = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
            dial_palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, transparent_color)
            dial_palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, transparent_color)
            dial_palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, transparent_color)
            dial_palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, transparent_color)
            dial_palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, transparent_color)
            dial_palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, transparent_color)
            dial.setPalette(dial_palette)
            dial.setOrigin(180+arc_bias) # Orient dial so 0 is at 9 o'clock
            dial.setScaleArc(min_val,max_val)
            dial.setRange(min_val, max_val, step)
            dial.setScale(min_val, max_val, step)
            dial.setScaleTicks(1,20,30)

            # Add needle
            color_index = int(str(i)[len(str(i))-1:len(str(i)):]) # get last digit of i
            if color_index == 0:
                needleColor = QtGui.QColor(255, 0, 0) # red
            elif color_index == 1:
                needleColor = QtGui.QColor(255, 125, 0) # orange
            elif color_index == 2:
                needleColor = QtGui.QColor(255, 255, 0) # yellow
            elif color_index == 3:
                needleColor = QtGui.QColor(0, 255, 0) # green
            elif color_index == 4:
                needleColor = QtGui.QColor(0, 255, 255) # light blue
            elif color_index == 5:
                needleColor = QtGui.QColor(0, 0, 255) # blue
            elif color_index == 6:
                needleColor = QtGui.QColor(255, 0, 255) # light purple
            elif color_index == 7:
                needleColor = QtGui.QColor(150, 0, 255) # purple
            elif color_index == 8:
                needleColor = QtGui.QColor(150, 100, 0) # brown
            else:
                needleColor = QtGui.QColor(0, 0, 0) # black
            dial.setNeedle(Qwt.QwtDialSimpleNeedle(
                Qwt.QwtDialSimpleNeedle.Arrow,
                True,
                needleColor,
                QtGui.QColor(QtCore.Qt.gray).light(130)))
            dial.setValue(0)

            # Set sizing
            dial.setMinimumSize(250,250)
            dial.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
            self.dial_list.append(dial)
            self.next_angles.append(0)

        # Add to overall layout
        for i in self.dial_list:
            self.compass_layout.addWidget(i,0,0)

        # Add label
        self.label = Qt.QLabel(label)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.this_layout.addWidget(self.label)
        self.this_layout.addLayout(self.compass_layout)

        self.label.raise_()

        # connect the plot callback signal
        QtCore.QObject.connect(self,
                       QtCore.SIGNAL("updatePlot(int)"),
                       self.do_plot)

    def trigger_update(self):
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)

    def do_plot(self, a):
        # Update qt plots
        for i in range(len(self.dial_list)):
            self.dial_list[i].setValue(self.next_angles[i])
            self.replot()

    def work(self, input_items, output_items):
        # Average inputs
        for i in range(len(self.next_angles)):
            self.next_angles[i] = numpy.mean(input_items[i])

        if (time.time() - self.last)>self.update_period:
            self.last = time.time()
            # trigger update
            self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)

        # Consume all inputs
        return len(input_items[0])
