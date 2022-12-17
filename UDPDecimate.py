#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Udpdecimate
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import cmath
import math
import osmosdr
import time

class UDPDecimate(gr.top_block):

    def __init__(self, final_decimation=4, gain=21, pulse_duration=0.015, pulse_freq=146000000, samp_rate=3e6):
        gr.top_block.__init__(self, "Udpdecimate")

        ##################################################
        # Parameters
        ##################################################
        self.final_decimation = final_decimation
        self.gain = gain
        self.pulse_duration = pulse_duration
        self.pulse_freq = pulse_freq
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.decimate_1 = decimate_1 = 15
        self.samp_rate2 = samp_rate2 = samp_rate/decimate_1
        self.decimate_2 = decimate_2 = 10
        self.samp_rate3 = samp_rate3 = samp_rate2/decimate_2
        self.taps3 = taps3 = firdes.low_pass(1.0, samp_rate3, 1.5e3,0.3e3, firdes.WIN_KAISER, 6.76 / 2)
        self.taps2 = taps2 = firdes.low_pass(1.0, samp_rate2, 1.5e3,16e3 - 1.5e3, firdes.WIN_BLACKMAN, 6.76)
        self.taps1 = taps1 = firdes.low_pass(1.0, samp_rate, 1.5e3,128e3 - 1.5e3, firdes.WIN_BLACKMAN, 6.76)
        self.decimate_3 = decimate_3 = 5
        self.taps3_len = taps3_len = len(taps3)
        self.taps2_len = taps2_len = len(taps2)
        self.taps1_len = taps1_len = len(taps1)
        self.samp_rate4 = samp_rate4 = samp_rate3/decimate_3

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'airspy=0,sensitivity'
        )
        self.osmosdr_source_0.set_clock_source('gpsdo', 0)
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(pulse_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decimate_1, taps1, 0, samp_rate)
        self.fir_filter_xxx_0_0_0 = filter.fir_filter_ccf(decimate_3, taps3)
        self.fir_filter_xxx_0_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0_0 = filter.fir_filter_ccf(decimate_2, taps2)
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_gr_complex*1, '127.0.0.1', 20000, 1472, True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.fir_filter_xxx_0_0, 0), (self.fir_filter_xxx_0_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))

    def get_final_decimation(self):
        return self.final_decimation

    def set_final_decimation(self, final_decimation):
        self.final_decimation = final_decimation

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.osmosdr_source_0.set_gain(self.gain, 0)

    def get_pulse_duration(self):
        return self.pulse_duration

    def set_pulse_duration(self, pulse_duration):
        self.pulse_duration = pulse_duration

    def get_pulse_freq(self):
        return self.pulse_freq

    def set_pulse_freq(self, pulse_freq):
        self.pulse_freq = pulse_freq
        self.osmosdr_source_0.set_center_freq(self.pulse_freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_rate2(self.samp_rate/self.decimate_1)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_decimate_1(self):
        return self.decimate_1

    def set_decimate_1(self, decimate_1):
        self.decimate_1 = decimate_1
        self.set_samp_rate2(self.samp_rate/self.decimate_1)

    def get_samp_rate2(self):
        return self.samp_rate2

    def set_samp_rate2(self, samp_rate2):
        self.samp_rate2 = samp_rate2
        self.set_samp_rate3(self.samp_rate2/self.decimate_2)

    def get_decimate_2(self):
        return self.decimate_2

    def set_decimate_2(self, decimate_2):
        self.decimate_2 = decimate_2
        self.set_samp_rate3(self.samp_rate2/self.decimate_2)

    def get_samp_rate3(self):
        return self.samp_rate3

    def set_samp_rate3(self, samp_rate3):
        self.samp_rate3 = samp_rate3
        self.set_samp_rate4(self.samp_rate3/self.decimate_3)

    def get_taps3(self):
        return self.taps3

    def set_taps3(self, taps3):
        self.taps3 = taps3
        self.set_taps3_len(len(self.taps3))
        self.fir_filter_xxx_0_0_0.set_taps(self.taps3)

    def get_taps2(self):
        return self.taps2

    def set_taps2(self, taps2):
        self.taps2 = taps2
        self.set_taps2_len(len(self.taps2))
        self.fir_filter_xxx_0_0.set_taps(self.taps2)

    def get_taps1(self):
        return self.taps1

    def set_taps1(self, taps1):
        self.taps1 = taps1
        self.set_taps1_len(len(self.taps1))
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.taps1)

    def get_decimate_3(self):
        return self.decimate_3

    def set_decimate_3(self, decimate_3):
        self.decimate_3 = decimate_3
        self.set_samp_rate4(self.samp_rate3/self.decimate_3)

    def get_taps3_len(self):
        return self.taps3_len

    def set_taps3_len(self, taps3_len):
        self.taps3_len = taps3_len

    def get_taps2_len(self):
        return self.taps2_len

    def set_taps2_len(self, taps2_len):
        self.taps2_len = taps2_len

    def get_taps1_len(self):
        return self.taps1_len

    def set_taps1_len(self, taps1_len):
        self.taps1_len = taps1_len

    def get_samp_rate4(self):
        return self.samp_rate4

    def set_samp_rate4(self, samp_rate4):
        self.samp_rate4 = samp_rate4


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--final-decimation", dest="final_decimation", type=intx, default=4,
        help="Set Final decimation [default=%(default)r]")
    parser.add_argument(
        "--gain", dest="gain", type=intx, default=21,
        help="Set Gain [default=%(default)r]")
    parser.add_argument(
        "--pulse-duration", dest="pulse_duration", type=eng_float, default="15.0m",
        help="Set Pulse duration (secs) [default=%(default)r]")
    parser.add_argument(
        "--pulse-freq", dest="pulse_freq", type=intx, default=146000000,
        help="Set Pulse Freq [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default="3.0M",
        help="Set Sample Rate [default=%(default)r]")
    return parser


def main(top_block_cls=UDPDecimate, options=None):
    if options is None:
        options = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")
    tb = top_block_cls(final_decimation=options.final_decimation, gain=options.gain, pulse_duration=options.pulse_duration, pulse_freq=options.pulse_freq, samp_rate=options.samp_rate)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
