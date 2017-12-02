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
class am_audio_decoder(gr.hier_block2):
    """
    docstring for block am_audio_decoder
    """
    def __init__(self, sign_freq, audio_freq, 
                 signal_low_pass_cutoff=10000, signal_low_pass_trans=1000,
                 audio_low_pass_cutoff=3000, audio_low_pass_trans=20,
                 use_dc_blocker=True, audio_gain=1):
        ##################################################
        # Variables
        ##################################################
        self.sign_freq = sign_freq
        self.audio_freq = audio_freq
        self.signal_low_pass_cutoff = signal_low_pass_cutoff
        self.signal_low_pass_trans = signal_low_pass_trans
        self.audio_low_pass_cutoff = audio_low_pass_cutoff
        self.audio_low_pass_trans = audio_low_pass_trans
        self.use_dc_blocker = use_dc_blocker
        self.audio_gain = audio_gain

        # hyper parameter
        self.low_pass_ampl_bound = 0.1
        self.low_pass_window = firdes.WIN_HAMMING
        self.low_pass_beta = 6.76

        ##################################################
        # Submodule
        ##################################################
        self.input_resample = filter.rational_resampler_ccf(interpolation=2000000,
                                                            decimation=sign_freq,
                                                            taps=None,
                                                            fractional_bw=None)
        
        self.signal_low_pass_filter = eewls.auto_gain_low_pass_filter(filter.fir_filter_ccf, 8, 
                                                                      self.low_pass_ampl_bound, 
                                                                      2000000, 
                                                                      self.signal_low_pass_cutoff, 
                                                                      self.signal_low_pass_trans,
                                                                      self.low_pass_window,
                                                                      self.low_pass_beta, 
                                                                      str(complex))

        self.am_demod = analog.am_demod_cf(channel_rate=50000, 
                                           audio_decim=5, 
                                           audio_pass=5000, 
                                           audio_stop=5500)
        self.resampler = filter.rational_resampler_fff(interpolation=48*self.audio_freq*2/96000,
                                                       decimation=50,
                                                       taps=None,
                                                       fractional_bw=None)
        self.audio_filter = filter.interp_fir_filter_fff(1, firdes.low_pass(self.audio_gain, 
                                                                            self.audio_freq*2, 
                                                                            self.audio_low_pass_cutoff, 
                                                                            self.audio_low_pass_trans, 
                                                                            self.low_pass_window,
                                                                            self.low_pass_beta))

        gr.hier_block2.__init__(self, "fm_audio_decoder",
                                gr.io_signature(1, 1, self.input_resample.input_signature().sizeof_stream_item(0)),
                                gr.io_signature(1, 1, self.audio_filter.output_signature().sizeof_stream_item(0)))

        if self.use_dc_blocker:
            self.dc_blocker = filter.dc_blocker_cc(256, True)
        ##################################################
        # Connections
        ##################################################
        self.connect((self, 0), (self.input_resample, 0))
        self.connect((self.input_resample, 0), (self.signal_low_pass_filter, 0))
        if self.use_dc_blocker:
            self.connect((self.signal_low_pass_filter, 0), (self.dc_blocker, 0))
            self.connect((self.dc_blocker, 0), (self.am_demod, 0))
        else:
            self.connect((self.signal_low_pass_filter, 0), (self.am_demod, 0))
        self.connect((self.am_demod, 0), (self.resampler, 0))
        self.connect((self.resampler, 0), (self.audio_filter, 0))
        self.connect((self.audio_filter, 0), (self, 0))

    def set_taps(self, signal_low_pass_cutoff, signal_low_pass_trans, 
                 audio_low_pass_cutoff, audio_low_pass_trans, audio_gain):
        
        if (signal_low_pass_cutoff != self.signal_low_pass_cutoff or 
                signal_low_pass_trans != self.signal_low_pass_trans):
            self.signal_low_pass_cutoff = signal_low_pass_cutoff
            self.signal_low_pass_trans = signal_low_pass_trans
            self.signal_low_pass_filter.set_taps(self.low_pass_ampl_bound, 
                                                 2000000, 
                                                 self.signal_low_pass_cutoff,
                                                 self.signal_low_pass_trans,
                                                 self.low_pass_window,
                                                 self.low_pass_beta)
        
        if (audio_low_pass_cutoff != self.audio_low_pass_cutoff or
                audio_low_pass_trans != self.audio_low_pass_trans or
                audio_gain != self.audio_gain):
            self.audio_low_pass_cutoff = audio_low_pass_cutoff
            self.audio_low_pass_trans  = audio_low_pass_trans
            self.audio_gain = audio_gain
            self.audio_filter.set_taps(firdes.low_pass(self.audio_gain, 
                                                       self.audio_freq*2, 
                                                       self.audio_low_pass_cutoff,
                                                       self.audio_low_pass_trans,
                                                       self.low_pass_window, 
                                                       self.low_pass_beta))


