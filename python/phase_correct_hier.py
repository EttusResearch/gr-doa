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

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import pmt
import numpy
import sys
import parser

def convert_phase_strings_to_floats(num):
    try:
        return float(num)
    except:
        return False

def read_config_file(filename):
    # Read phase(s) from configuration file
    lines = [line.rstrip('\n') for line in open(filename,'r')]
    strings = filter(convert_phase_strings_to_floats,lines)
    return [float(s) for s in strings]


def gen_sig_io(num_elements,sig_type):
    # Dynamically create types for signature
    io = []
    for i in range(num_elements):
        io.append(sig_type*1)
    return io

class phase_correct_hier(gr.hier_block2):

    def __init__(self, num_ports=2, config_filename=''):
        gr.hier_block2.__init__(
            self, "Phase Correct Chains",
            gr.io_signaturev(num_ports, num_ports, gen_sig_io(num_ports,gr.sizeof_gr_complex)),
            gr.io_signaturev(num_ports, num_ports, gen_sig_io(num_ports,gr.sizeof_gr_complex)),
        )

        ##################################################
        # Parameters
        ##################################################
        self.num_ports = num_ports
        self.config_filename = config_filename
        # Check file
        try:
            file = open(self.config_filename, 'r')
            file.close()
        except:
            sys.stderr.write("Configuration "+config_filename+", not valid\n")
            print(sys.stderr)
            sys.exit(1)
        # Check that we have enough measurments
        self.phases = read_config_file(config_filename)
        if len(self.phases)!=(num_ports-1):
            sys.stderr.write("Configuration "+config_filename+". Not valid number of phase estimates\n")
            print(sys.stderr)
            sys.exit(1)

        ##################################################
        # Blocks
        ##################################################

        # Connect first signal directly to output
        self.nop = blocks.copy(gr.sizeof_gr_complex*1)
        self.nop.set_enabled(True)
        self.connect((self, 0), self.nop)
        self.connect(self.nop, (self, 0))

        for p in range(num_ports-1):
            ## Add blocks
            # Place multiply object
            object_name_mc = 'multiply_const_'+str(p)
            gain = numpy.exp(1j*self.phases[p])
            setattr(self, object_name_mc, blocks.multiply_const_vcc((gain,)))

            ## Make Connections
            # Top to multiply
            self.connect((self, p+1), (getattr(self,object_name_mc), 0))
            # Multiply to top
            self.connect((getattr(self,object_name_mc), 0), (self,p+1))
