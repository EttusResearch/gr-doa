#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Ettus Research LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import pmt
import numpy
import sys

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
    """
    Correct phase offsets of N complex input channels, provided
    in a specified configuration file.
    """
    def __init__(self, num_ports, config_filename):
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

