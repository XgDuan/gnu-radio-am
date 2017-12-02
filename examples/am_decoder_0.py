#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Am Decoder 0
# Generated: Thu Nov 30 13:51:16 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import baz
import eewls
import sys


class am_decoder_0(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Am Decoder 0")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Am Decoder 0")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "am_decoder_0")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.trans_width = trans_width = 1000
        self.sound_filter_transwidth = sound_filter_transwidth = 20
        self.sound_filter_cutoff = sound_filter_cutoff = 2000
        self.samp_rate = samp_rate = 2000000
        self.cutoff = cutoff = 10000
        self.channel_freq = channel_freq = 127740000

        ##################################################
        # Blocks
        ##################################################
        self._trans_width_range = Range(0, 200000, 100, 1000, 200)
        self._trans_width_win = RangeWidget(self._trans_width_range, self.set_trans_width, "trans_width", "counter_slider", float)
        self.top_layout.addWidget(self._trans_width_win)
        self._sound_filter_transwidth_range = Range(1, 5000, 20, 20, 2005000)
        self._sound_filter_transwidth_win = RangeWidget(self._sound_filter_transwidth_range, self.set_sound_filter_transwidth, 'sound_filter_transwidth', "counter_slider", float)
        self.top_layout.addWidget(self._sound_filter_transwidth_win)
        self._sound_filter_cutoff_range = Range(1000, 5000, 20, 2000, 200)
        self._sound_filter_cutoff_win = RangeWidget(self._sound_filter_cutoff_range, self.set_sound_filter_cutoff, 'sound_filter_cutoff', "counter_slider", float)
        self.top_layout.addWidget(self._sound_filter_cutoff_win)
        self._cutoff_range = Range(0, 200000, 100, 10000, 200)
        self._cutoff_win = RangeWidget(self._cutoff_range, self.set_cutoff, "cutoff", "counter_slider", float)
        self.top_layout.addWidget(self._cutoff_win)
        self._channel_freq_range = Range(0, 140000000, 20000, 127740000, 200)
        self._channel_freq_win = RangeWidget(self._channel_freq_range, self.set_channel_freq, 'channel_freq', "counter_slider", float)
        self.top_layout.addWidget(self._channel_freq_win)
        self.rtl_source = baz.rtl_source_c(defer_creation=True, output_size=gr.sizeof_gr_complex)
        self.rtl_source.set_verbose(True)
        self.rtl_source.set_vid(0x0)
        self.rtl_source.set_pid(0x0)
        self.rtl_source.set_tuner_name('r820t')
        self.rtl_source.set_default_timeout(0)
        self.rtl_source.set_use_buffer(True)
        self.rtl_source.set_fir_coefficients(([]))
        
        self.rtl_source.set_read_length(0)
        
        
        
        
        if self.rtl_source.create() == False: raise Exception("Failed to create RTL2832 Source: rtl_source")
        
        self.rtl_source.set_bandwidth(100000)
        
        self.rtl_source.set_sample_rate(samp_rate)
        
        self.rtl_source.set_frequency(channel_freq)
        
        
        
        self.rtl_source.set_auto_gain_mode(True)
        self.rtl_source.set_relative_gain(True)
        self.rtl_source.set_gain(200)
          
        self.resampler = filter.rational_resampler_fff(
                interpolation=48,
                decimation=50,
                taps=None,
                fractional_bw=None,
        )
        self.multiply_const_0 = blocks.multiply_const_vff((1, ))
        self.low_pass_filter_0 = filter.interp_fir_filter_fff(1, firdes.low_pass(
        	1, 96000, sound_filter_cutoff, sound_filter_transwidth, firdes.WIN_HAMMING, 6.76))
        self.dc_blocker_xx_0 = filter.dc_blocker_cc(256, True)
        self.auto_gain_low_pass_filter_0 = eewls.auto_gain_low_pass_filter(filter.fir_filter_ccf, 1, 0.5, samp_rate, cutoff, trans_width, firdes.WIN_HAMMING, 6.76, str(complex))
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.am_demod = analog.am_demod_cf(
        	channel_rate=50000,
        	audio_decim=5,
        	audio_pass=5000,
        	audio_stop=5500,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.am_demod, 0), (self.resampler, 0))    
        self.connect((self.auto_gain_low_pass_filter_0, 0), (self.dc_blocker_xx_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.am_demod, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.multiply_const_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.resampler, 0), (self.multiply_const_0, 0))    
        self.connect((self.rtl_source, 0), (self.auto_gain_low_pass_filter_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "am_decoder_0")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_trans_width(self):
        return self.trans_width

    def set_trans_width(self, trans_width):
        self.trans_width = trans_width
        self.auto_gain_low_pass_filter_0.set_taps(0.5, self.samp_rate, self.cutoff, self.trans_width, firdes.WIN_HAMMING, 6.76)

    def get_sound_filter_transwidth(self):
        return self.sound_filter_transwidth

    def set_sound_filter_transwidth(self, sound_filter_transwidth):
        self.sound_filter_transwidth = sound_filter_transwidth
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, 96000, self.sound_filter_cutoff, self.sound_filter_transwidth, firdes.WIN_HAMMING, 6.76))

    def get_sound_filter_cutoff(self):
        return self.sound_filter_cutoff

    def set_sound_filter_cutoff(self, sound_filter_cutoff):
        self.sound_filter_cutoff = sound_filter_cutoff
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, 96000, self.sound_filter_cutoff, self.sound_filter_transwidth, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtl_source.set_sample_rate(self.samp_rate)
        self.auto_gain_low_pass_filter_0.set_taps(0.5, self.samp_rate, self.cutoff, self.trans_width, firdes.WIN_HAMMING, 6.76)

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff
        self.auto_gain_low_pass_filter_0.set_taps(0.5, self.samp_rate, self.cutoff, self.trans_width, firdes.WIN_HAMMING, 6.76)

    def get_channel_freq(self):
        return self.channel_freq

    def set_channel_freq(self, channel_freq):
        self.channel_freq = channel_freq
        self.rtl_source.set_frequency(self.channel_freq)


def main(top_block_cls=am_decoder_0, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
