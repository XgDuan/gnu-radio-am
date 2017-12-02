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
import threading
import time

import numpy as np

from gnuradio import gr
from gnuradio import blocks
from gnuradio import fft
from gnuradio import analog
from gnuradio.fft import window

class freq_selector(gr.hier_block2):
    """
    docstring for block freq_selector
    """
    def __init__(self, base_freq, samp_rate, num_output, 
                 use_fixed_freq, freq_1,freq_2, freq_3):

        freq_1 = base_freq if freq_1 == -1 else freq_1
        freq_2 = base_freq if freq_2 == -1 else freq_2
        freq_3 = base_freq if freq_3 == -1 else freq_3
        
        if use_fixed_freq:
            if num_output == 1:
                if freq_2 != base_freq and freq_3 != base_freq:
                    gr.log.info('num_output(%d)<given freq, freq_2, freq_3 will be overlooked'%num_output)
                if freq_1 > base_freq + samp_rate/2 or freq_1 < base_freq - samp_rate/2:
                    gr.log.info('given freq(%d), exceed freq_range(%d->%d), use auto_freq instead'%(freq_1, base_freq - samp_rate/2, base_freq + samp_rate/2))
                    freq_1 = base_freq
            if num_output == 2:
                if freq_3 != base_freq:
                    gr.log.info('num_output(%d)<given freq, freq_2, freq_3 will be overlooked'%num_output)
                if freq_1 > base_freq + samp_rate/2 or freq_1 < base_freq - samp_rate/2:
                    gr.log.info('given freq(%d), exceed freq_range(%d->%d), use auto_freq instead'%(freq_1, base_freq - samp_rate/2, base_freq + samp_rate/2))
                    freq_1 = base_freq
                if freq_2 > base_freq + samp_rate/2 or freq_2 < base_freq - samp_rate/2:
                    gr.log.info('given freq(%d), exceed freq_range(%d->%d), use auto_freq instead'%(freq_2, base_freq - samp_rate/2, base_freq + samp_rate/2))
                    freq_2 = base_freq            
            if num_output == 3:
                if freq_1 > base_freq + samp_rate/2 or freq_1 < base_freq - samp_rate/2:
                    gr.log.info('given freq(%d), exceed freq_range(%d->%d), use auto_freq instead'%(freq_1, base_freq - samp_rate/2, base_freq + samp_rate/2))
                    freq_1 = base_freq
                if freq_2 > base_freq + samp_rate/2 or freq_2 < base_freq - samp_rate/2:
                    gr.log.info('given freq(%d), exceed freq_range(%d->%d), use auto_freq instead'%(freq_2, base_freq - samp_rate/2, base_freq + samp_rate/2))
                    freq2 = base_freq
                if freq_3 > base_freq + samp_rate/2 or freq_3 < base_freq - samp_rate/2:
                    gr.log.info('given freq(%d), exceed freq_range(%d->%d), use auto_freq instead'%(freq_3, base_freq - samp_rate/2, base_freq + samp_rate/2))
                    freq_3 = base_freq
        ##################################################
        # Variables
        ##################################################
        self.base_freq = base_freq
        self.samp_rate = samp_rate
        self.num_output = num_output
        self.use_fixed_freq = use_fixed_freq
        self.freq_1 = freq_1
        self.freq_2 = freq_2
        self.freq_3 = freq_3
        self.fft_val = None

        ##################################################
        # Submodule
        ##################################################
        self.signal_sources = [analog.sig_source_c(self.samp_rate, analog.GR_COS_WAVE, getattr(self, 'freq_%d'%(i+1) ) - self.base_freq, 1, 0) for i in range(self.num_output)]
        self.multiplies = [blocks.multiply_vcc(1) for i in range(self.num_output)]
        # freq selector
        self.stream_to_vector = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1024)
        self.fft = fft.fft_vcc(1024, True, (window.blackmanharris(1024)), True, 1)
        # self.vec_sink =  blocks.vector_sink_c(1024)
        self.samp_prob = blocks.probe_signal_vc(1024)

        gr.hier_block2.__init__(self,"freq_selector",
                                gr.io_signature(1, 1, gr.sizeof_gr_complex), # Input signature
                                gr.io_signature(1, 1, gr.sizeof_gr_complex),
                                ) # Output signature

        def _auto_freq_topk():
            while True:
                try:
                    # gr.log.info('0 set new max_freq:%d'%self.freq_1)
                    val = self.samp_prob.level()
                    # gr.log.info('1 set new max_freq:%d'%self.freq_1)
                    val = np.abs(np.array(val))
                    if self.fft_val is None:
                        self.fft_val = val
                    else:
                        self.fft_val = self.fft_val*0.9 + val * 0.1
                    amp_idx = np.argmax(self.fft_val)
                    freq_1 = self.base_freq - self.samp_rate/2 + (amp_idx)/1024*self.samp_rate
                    if freq_1 != self.freq_1:
                        pass
                        # self.set_taps(self.base_freq, self.samp_rate, freq_1)
                        # gr.log.info('set new max_freq as %d for the %dth num of fft'%(self.freq_1, amp_idx))
                except AttributeError:
                    pass
                time.sleep(1.0 / (10000))
        _auto_freq_topk_thread = threading.Thread(target=_auto_freq_topk)
        _auto_freq_topk_thread.daemon = True
        _auto_freq_topk_thread.start()

        for i in range(self.num_output):
            self.connect((self, 0), (self.multiplies[i], 0))
            self.connect((self.signal_sources[i], 0), (self.multiplies[i], 1))
            self.connect((self.multiplies[i], 0), (self, i))
        self.connect((self, 0), (self.stream_to_vector, 0))
        self.connect((self.stream_to_vector, 0), (self.fft, 0))
        self.connect((self.fft, 0), (self.samp_prob, 0))
        # self.connect((self.fft, 0), (self.fft_prob, 0))

    def set_taps(self, base_freq, samp_rate, freq_1):
        if freq_1 != self.freq_1 or base_freq != self.base_freq:
            self.freq_1 = freq_1
            self.base_freq = base_freq
            self.signal_sources[0].set_frequency(self.freq_1 - self.base_freq)
        if samp_rate != self.samp_rate:
            self.samp_rate = samp_rate
            self.signal_sources[0].set_sampling_freq(self.samp_rate)