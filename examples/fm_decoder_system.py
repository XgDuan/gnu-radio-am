#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Fm Decoder System
# Generated: Thu Nov 30 14:15:57 2017
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
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import baz
import eewls
import sip
import sys


class fm_decoder_system(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Fm Decoder System")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Fm Decoder System")
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

        self.settings = Qt.QSettings("GNU Radio", "fm_decoder_system")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2000000
        self.low_pass_trans = low_pass_trans = 5000
        self.low_pass_cutoff = low_pass_cutoff = 75000
        self.channel_freq = channel_freq = 103900000

        ##################################################
        # Blocks
        ##################################################
        self._low_pass_trans_range = Range(0, 200000, 500, 5000, 200)
        self._low_pass_trans_win = RangeWidget(self._low_pass_trans_range, self.set_low_pass_trans, "low_pass_trans", "counter_slider", float)
        self.top_layout.addWidget(self._low_pass_trans_win)
        self._low_pass_cutoff_range = Range(0, 100000, 500, 75000, 200)
        self._low_pass_cutoff_win = RangeWidget(self._low_pass_cutoff_range, self.set_low_pass_cutoff, "low_pass_cutoff", "counter_slider", float)
        self.top_layout.addWidget(self._low_pass_cutoff_win)
        self._channel_freq_range = Range(78000000, 108000000, 500, 103900000, 200)
        self._channel_freq_win = RangeWidget(self._channel_freq_range, self.set_channel_freq, "channel_freq", "counter_slider", float)
        self.top_layout.addWidget(self._channel_freq_win)
        self.rtl2832_source_0 = baz.rtl_source_c(defer_creation=True, output_size=gr.sizeof_gr_complex)
        self.rtl2832_source_0.set_verbose(True)
        self.rtl2832_source_0.set_vid(0x0)
        self.rtl2832_source_0.set_pid(0x0)
        self.rtl2832_source_0.set_tuner_name('r820t')
        self.rtl2832_source_0.set_default_timeout(0)
        self.rtl2832_source_0.set_use_buffer(True)
        self.rtl2832_source_0.set_fir_coefficients(([]))
        
        self.rtl2832_source_0.set_read_length(0)
        
        
        
        
        if self.rtl2832_source_0.create() == False: raise Exception("Failed to create RTL2832 Source: rtl2832_source_0")
        
        
        self.rtl2832_source_0.set_sample_rate(samp_rate)
        
        self.rtl2832_source_0.set_frequency(channel_freq)
        
        
        
        self.rtl2832_source_0.set_auto_gain_mode(True)
        self.rtl2832_source_0.set_relative_gain(True)
        self.rtl2832_source_0.set_gain(20)
          
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=50,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_sink_x_1 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate/8, #bw
        	"ors", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_1_win)
        
        self.qtgui_sink_x_1.enable_rf_freq(False)
        
        
          
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((0.5, ))
        self.auto_gain_low_pass_filter_0 = eewls.auto_gain_low_pass_filter(filter.fir_filter_ccf, 8, 0.5, samp_rate, low_pass_cutoff, low_pass_trans, firdes.WIN_HAMMING, 6.76, str(complex))
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=500000,
        	audio_decimation=5,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.auto_gain_low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.auto_gain_low_pass_filter_0, 0), (self.qtgui_sink_x_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.rtl2832_source_0, 0), (self.auto_gain_low_pass_filter_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fm_decoder_system")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtl2832_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate/8)
        self.auto_gain_low_pass_filter_0.set_taps(0.5, self.samp_rate, self.low_pass_cutoff, self.low_pass_trans, firdes.WIN_HAMMING, 6.76)

    def get_low_pass_trans(self):
        return self.low_pass_trans

    def set_low_pass_trans(self, low_pass_trans):
        self.low_pass_trans = low_pass_trans
        self.auto_gain_low_pass_filter_0.set_taps(0.5, self.samp_rate, self.low_pass_cutoff, self.low_pass_trans, firdes.WIN_HAMMING, 6.76)

    def get_low_pass_cutoff(self):
        return self.low_pass_cutoff

    def set_low_pass_cutoff(self, low_pass_cutoff):
        self.low_pass_cutoff = low_pass_cutoff
        self.auto_gain_low_pass_filter_0.set_taps(0.5, self.samp_rate, self.low_pass_cutoff, self.low_pass_trans, firdes.WIN_HAMMING, 6.76)

    def get_channel_freq(self):
        return self.channel_freq

    def set_channel_freq(self, channel_freq):
        self.channel_freq = channel_freq
        self.rtl2832_source_0.set_frequency(self.channel_freq)


def main(top_block_cls=fm_decoder_system, options=None):

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
