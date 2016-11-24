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

    def __init__(self, label="", min_val=-90, max_val=90, step=10, arc_bias=0, *args):
        gr.sync_block.__init__(self,name="QT Compass",in_sig=[numpy.float32],out_sig=[])
        Qwt.QwtPlot.__init__(self, *args)

        # Set parameters
        self.update_period = 0.1
        self.last = time.time()
        self.next_angle = 0

        ### QT STUFF

        # Setup overall layouts
        self.this_layout = Qt.QVBoxLayout()
        self.compass_layout = Qt.QGridLayout()

        # Setup Dial
        self.dial = Qwt.QwtDial(self)
        self.dial.setOrigin(180+arc_bias) # Orient dial so 0 is at 9 o'clock
        self.dial.setScaleArc(min_val,max_val)
        self.dial.setRange(min_val, max_val, step)
        self.dial.setScale(min_val ,max_val, step)
        self.dial.setScaleTicks(1,20,30)

        # Add needle
        self.dial.setNeedle(Qwt.QwtDialSimpleNeedle(
            Qwt.QwtDialSimpleNeedle.Arrow,
            True,
            QtGui.QColor(QtCore.Qt.red),
            QtGui.QColor(QtCore.Qt.gray).light(130)))
        self.dial.setValue(0)

        # Set sizing
        self.dial.setMinimumSize(250,250)
        self.dial.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)

        # Add to overall layout
        self.compass_layout.addWidget(self.dial,0,0)

        # Add label
        self.label = Qt.QLabel(label)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.this_layout.addWidget(self.label)
        self.this_layout.addLayout(self.compass_layout)

        # Setup LCD
        lcd_layout = Qt.QGridLayout()

        self.lcd = QtGui.QLCDNumber(self)
        sizePolicy = Qt.QSizePolicy(Qt.QSizePolicy.Preferred, Qt.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.lcd.setSizePolicy(sizePolicy)
        self.lcd.setLineWidth(0)

        # Set sizing
        self.lcd.setMinimumHeight(self.dial.minimumHeight()/2)
        self.lcd.setMinimumWidth(self.dial.minimumWidth()/2)

        self.lcd.raise_() # Bring to front
        self.lcd.setDigitCount(3) # Max digits displayed
        self.lcd.setSmallDecimalPoint(True)
        self.lcd.display(123.4)
        self.compass_layout.addLayout(lcd_layout,0,0)
        lcd_layout.addWidget(self.lcd,1,1,1,1)

        # Add spacers to center LCD
        spacerTop = QtGui.QSpacerItem(1,300,Qt.QSizePolicy.Maximum,Qt.QSizePolicy.Expanding)
        spacerSides = QtGui.QSpacerItem(220,1,Qt.QSizePolicy.Maximum,Qt.QSizePolicy.Expanding)
        spacerBottom = QtGui.QSpacerItem(1,150,Qt.QSizePolicy.Maximum,Qt.QSizePolicy.Expanding)
        # Top Spacers
        lcd_layout.addItem(spacerTop,0,1,1,1)
        # Side Spacers
        lcd_layout.addItem(spacerSides,1,0,1,1)
        lcd_layout.addItem(spacerSides,1,2,1,1)
        # Bottom Spacers
        lcd_layout.addItem(spacerBottom,2,1,1,1)

        self.label.raise_()

        # connect the plot callback signal
        QtCore.QObject.connect(self,
                       QtCore.SIGNAL("updatePlot(int)"),
                       self.do_plot)

    def change_angle(self,angle):
        self.dial.setValue(float(angle))

    def trigger_update(self):
        self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)

    def do_plot(self, a):
        # Update qt plots
        self.change_angle(self.next_angle)
        self.lcd.display(self.next_angle)
        self.replot()

    def work(self, input_items, output_items):
        # Average inputs
        self.next_angle = numpy.mean(input_items[0])

        if (time.time() - self.last)>self.update_period:
            self.last = time.time()
            # trigger update
            self.emit(QtCore.SIGNAL("updatePlot(int)"), 0)

        # Consume all inputs
        return len(input_items[0])
