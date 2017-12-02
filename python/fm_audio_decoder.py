#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr
from gnuradio import filter
from gnuradio import analog
from gnuradio.filter import firdes

import eewls

class fm_audio_decoder(gr.hier_block2):
    """
    docstring for block fm_audio_decoder
    """
    def __init__(self, sign_freq, audio_freq):

        ##################################################
        # Variables
        ##################################################
        self.sign_freq = sign_freq
        self.audio_freq = audio_freq

        # hyperparameter
        self.low_pass_cut_off = 75000
        self.low_pass_trans_width = 5000
        self.low_pass_ampl_bound = 0.5
        self.low_pass_window = firdes.WIN_HAMMING
        self.low_pass_beta = 6.76
        
        ##################################################
        # Submodule
        ##################################################

        # we always resample the signal frequency into 2MHz
        self.input_resample = filter.rational_resampler_ccf(interpolation=2000000,
                                                            decimation=sign_freq,
                                                            taps=None,
                                                            fractional_bw=None)

        self.low_pass_filter = eewls.auto_gain_low_pass_filter(filter.fir_filter_ccf, 8, 
                                                               self.low_pass_ampl_bound, 
                                                               2000000, 
                                                               self.low_pass_cut_off, 
                                                               self.low_pass_trans_width,
                                                               self.low_pass_window,
                                                               self.low_pass_beta, 
                                                               str(complex))

        self.analog_wfm_rcv = analog.wfm_rcv(quad_rate=500000, audio_decimation=5)
        
        self.rational_resampler = filter.rational_resampler_fff(interpolation=48,
                                                                decimation=50,
                                                                taps=None,
                                                                fractional_bw=None)
        
        gr.hier_block2.__init__(self, "fm_audio_decoder",
                                gr.io_signature(1, 1, self.input_resample.input_signature().sizeof_stream_item(0)),
                                gr.io_signature(1, 1, self.rational_resampler.output_signature().sizeof_stream_item(0)))

        ##################################################
        # Connections
        ##################################################
        self.connect((self, 0), (self.input_resample, 0))
        self.connect((self.input_resample, 0), (self.low_pass_filter, 0))
        self.connect((self.low_pass_filter, 0), (self.analog_wfm_rcv, 0))
        self.connect((self.analog_wfm_rcv, 0), (self.rational_resampler, 0))
        self.connect((self.rational_resampler, 0), (self, 0))