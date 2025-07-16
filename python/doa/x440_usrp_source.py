#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Ettus Research LLC.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#



from gnuradio import gr
from gnuradio import uhd


def gen_sig_io(num_elements):
    # Dynamically create types for signature
    io = []
    for i in range(num_elements):
        io.append(gr.sizeof_gr_complex*1)
    io.append(gr.sizeof_float*num_elements)
    return io

class x440_usrp_source(gr.hier_block2):
    """
    USRP X440 Source Block
    
    This block provides a source interface for the USRP X440 device.
    It configures multiple channels for synchronized reception and handles
    proper frequency tuning and LO distribution.
    
    Parameters:
        samp_rate (float): Sample rate in samples per second
        center_freq (float): Center frequency in Hz
        gain (float): RX gain in dB
        sources (int): Number of source channels to enable
        addresses (str): Device address (e.g., "addr=192.168.10.2")
        device_args (str): Additional device arguments
    """
    def __init__(self, samp_rate, center_freq, gain, sources, addresses, device_args):
        gr.hier_block2.__init__(self,
            "x440_usrp_source",
            gr.io_signature(0, 0, 0),
            gr.io_signaturev(sources, sources, gen_sig_io(sources)),
        ) 


        ##################################################
        # Parameters
        ##################################################
        self.samp_rate = samp_rate
        self.center_freq = center_freq
        self.gain = gain
        self.sources = sources
        self.addresses = addresses
        self.device_args = device_args

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join((self.addresses, self.device_args)),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(sources),
        	),
        )

        self.uhd_usrp_source_0.set_clock_source('internal', 0)
        self.uhd_usrp_source_0.set_time_source('internal', 0)


        # Subdevice-Spezifikation für 8 Kanäle (2 Boards à 4 Kanäle)
        subdevs = 'A:0 A:1 A:2 A:3 B:0 B:1 B:2 B:3'.split(' ')
        self.uhd_usrp_source_0.set_subdev_spec(' '.join(subdevs[:sources]), 0)

        # Set sample rate
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)

        # Set time to unknown PPS (für Synchronisation)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())

        # Konfiguration der Kanäle
        for chan in range(sources):
            self.uhd_usrp_source_0.set_gain(gain, chan)
            # change the interface here if you want to use a different antenna
            self.uhd_usrp_source_0.set_antenna("TX/RX", chan)

        # Use timed commands to set frequencies
        self.set_center_freq(center_freq, sources)

        ##################################################
        # Connections
        ##################################################
        for source in range(sources):
            self.connect((self.uhd_usrp_source_0, source), (self, source))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def set_center_freq(self, center_freq, sources):
        # Synchronize the tuned channels (if needed for x440)
        now = self.uhd_usrp_source_0.get_time_now()
        self.uhd_usrp_source_0.set_command_time(now + uhd.time_spec(0.01))
        # Tune all channels to the desired frequency for x440
        for chan in range(sources):
            self.uhd_usrp_source_0.set_center_freq(center_freq, chan)


        self.uhd_usrp_source_0.clear_command_time()

    def get_center_freq(self):
        return self.center_freq

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_sources(self):
        return self.sources

    def set_sources(self, sources):
        self.sources = sources