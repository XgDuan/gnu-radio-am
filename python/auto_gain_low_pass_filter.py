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
from gnuradio import gr, gru
from gnuradio import filter
from gnuradio import blocks
from gnuradio.filter import firdes

import numpy as np

class auto_gain_low_pass_filter(gr.hier_block2):
    """
    base class for all auto gain low pass filters
    """
    def __init__(self, fliter_base,
                 intep_deci, auto_gain, samp_rate, 
                 cutoff_freq, trans_width, window, beta, dtype):
        """
        Args:
            [TODO]: complete args docstring.
        """

        self.gain_ratio = auto_gain
        self.lp_gain = np.float64(1)
        self.samp_rate = samp_rate
        self.cutoff_freq = cutoff_freq
        self.trans_width = trans_width
        self.window = window
        self.beta = beta
        self.amp_gain = None

        self.filter = fliter_base(intep_deci, firdes.low_pass(self.lp_gain, samp_rate, cutoff_freq, trans_width, window, beta))
        
        if str(dtype) == "<type 'complex'>":
            gr.log.info("init auto gain low pass filter with complex type")
            self.samp_vector = blocks.stream_to_vector(gr.sizeof_gr_complex, 1024)
            self.samp_prob = blocks.probe_signal_vc(1024)
        else:
            gr.log.info("init auto gain low pass filter with float type")
            self.samp_vector = blocks.stream_to_vector(gr.sizeof_float, 1024)
            self.samp_prob = blocks.probe_signal_vf(1024)

        gr.hier_block2.__init__(self, "rational_resampler",
                    gr.io_signature(1, 1, self.filter.input_signature().sizeof_stream_item(0)),
                    gr.io_signature(1, 1, self.filter.output_signature().sizeof_stream_item(0)))


        def _auto_gain_function_probe():
            while True:
                try:
                    val = self.samp_prob.level()
                    val = np.abs(np.array(val))
                    amp_pp = max(val)
                    if amp_pp > 0:
                        if self.amp_gain is None:
                            self.amp_gain = (self.gain_ratio/amp_pp)
                        if abs(self.gain_ratio/amp_pp -1) > 0.2:
                            self.amp_gain += (self.gain_ratio/amp_pp -1)*self.amp_gain
                            # gr.log.info('current gain:%f, target: %f.'%(self.get_lp_gain(), self.amp_gain))
                            self.set_lp_gain(self.amp_gain)
                    # print(amp_pp)
                    # print(amp_pp/0.5)
                except AttributeError:
                    pass
                time.sleep(1.0 / (100))
        _auto_gain_function_thread = threading.Thread(target=_auto_gain_function_probe)
        _auto_gain_function_thread.daemon = True
        _auto_gain_function_thread.start()

        # connections
        self.connect((self.filter, 0), (self.samp_vector, 0))
        self.connect((self.samp_vector, 0), (self.samp_prob, 0))
        self.connect(self, self.filter, self)

    def get_lp_gain(self):
        return self.lp_gain

    def set_lp_gain(self, lp_gain):
        self.lp_gain = np.float64(lp_gain)
        self.filter.set_taps(firdes.low_pass(self.lp_gain, self.samp_rate, self.cutoff_freq, self.trans_width, self.window, self.beta))

    def taps(self):
        return self.resampler.taps()

    def set_taps(self, auto_gain, samp_rate, cutoff_freq, trans_width, window, beta):
        self.gain_ratio = auto_gain
        self.samp_rate = samp_rate
        self.cutoff_freq = cutoff_freq
        self.trans_width = trans_width
        self.window = window
        self.beta = beta
        self.filter.set_taps(firdes.low_pass(self.lp_gain, self.samp_rate, self.cutoff_freq, self.trans_width, self.window, self.beta))
