#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Am Audio Decoder 1
# Generated: Thu Nov 30 16:41:27 2017
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


class am_audio_decoder_1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Am Audio Decoder 1")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Am Audio Decoder 1")
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

        self.settings = Qt.QSettings("GNU Radio", "am_audio_decoder_1")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.signal_freq = signal_freq = 126000000
        self.signal_freq_2 = signal_freq_2 = signal_freq
        self.signal_freq_1 = signal_freq_1 = signal_freq
        self.signal_freq_0 = signal_freq_0 = 125800000
        self.samp_rate = samp_rate = 2000000

        ##################################################
        # Blocks
        ##################################################
        self._signal_freq_range = Range(120000000, 140000000, 500, 126000000, 200)
        self._signal_freq_win = RangeWidget(self._signal_freq_range, self.set_signal_freq, "signal_freq", "counter_slider", float)
        self.top_layout.addWidget(self._signal_freq_win)
        self._signal_freq_2_range = Range(signal_freq-samp_rate/2, signal_freq+samp_rate/2, 500, signal_freq, 200)
        self._signal_freq_2_win = RangeWidget(self._signal_freq_2_range, self.set_signal_freq_2, "signal_freq_2", "counter_slider", float)
        self.top_layout.addWidget(self._signal_freq_2_win)
        self._signal_freq_1_range = Range(signal_freq - samp_rate/2, signal_freq+samp_rate/2, 500, signal_freq, 200)
        self._signal_freq_1_win = RangeWidget(self._signal_freq_1_range, self.set_signal_freq_1, "signal_freq_1", "counter_slider", float)
        self.top_layout.addWidget(self._signal_freq_1_win)
        self._signal_freq_0_range = Range(signal_freq-samp_rate/2, signal_freq+samp_rate/2, 500, 125800000, 200)
        self._signal_freq_0_win = RangeWidget(self._signal_freq_0_range, self.set_signal_freq_0, "signal_freq_0", "counter_slider", float)
        self.top_layout.addWidget(self._signal_freq_0_win)
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
        
        self.rtl_source.set_frequency(signal_freq)
        
        
        
        self.rtl_source.set_auto_gain_mode(True)
        self.rtl_source.set_relative_gain(True)
        self.rtl_source.set_gain(200)
          
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	signal_freq, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        
        self.qtgui_sink_x_0.enable_rf_freq(False)
        
        
          
        self.eewls_am_audio_decoder_0_0_1 = eewls.am_audio_decoder(samp_rate, 48000, 
                                       50000, 5000,
                                       5000, 1000,
                                       1, 0.5)
        self.eewls_am_audio_decoder_0_0_0 = eewls.am_audio_decoder(samp_rate, 48000, 
                                       50000, 5000,
                                       5000, 1000,
                                       1, 0.5)
        self.eewls_am_audio_decoder_0_0 = eewls.am_audio_decoder(samp_rate, 48000, 
                                       50000, 5000,
                                       5000, 1000,
                                       1, 0.5)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, signal_freq_2 - signal_freq, 1, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, signal_freq_0 - signal_freq, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, signal_freq_1 - signal_freq, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0_0, 1))    
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_multiply_xx_0_0, 1))    
        self.connect((self.blocks_add_xx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.eewls_am_audio_decoder_0_0_1, 0))    
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.eewls_am_audio_decoder_0_0_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.eewls_am_audio_decoder_0_0, 0))    
        self.connect((self.eewls_am_audio_decoder_0_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.eewls_am_audio_decoder_0_0_0, 0), (self.blocks_add_xx_0, 2))    
        self.connect((self.eewls_am_audio_decoder_0_0_1, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.rtl_source, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.rtl_source, 0), (self.blocks_multiply_xx_0_0, 0))    
        self.connect((self.rtl_source, 0), (self.blocks_multiply_xx_0_0_0, 0))    
        self.connect((self.rtl_source, 0), (self.qtgui_sink_x_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "am_audio_decoder_1")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_signal_freq(self):
        return self.signal_freq

    def set_signal_freq(self, signal_freq):
        self.signal_freq = signal_freq
        self.set_signal_freq_2(self.signal_freq)
        self.set_signal_freq_1(self.signal_freq)
        self.rtl_source.set_frequency(self.signal_freq)
        self.qtgui_sink_x_0.set_frequency_range(self.signal_freq, self.samp_rate)
        self.analog_sig_source_x_0_1.set_frequency(self.signal_freq_2 - self.signal_freq)
        self.analog_sig_source_x_0_0.set_frequency(self.signal_freq_0 - self.signal_freq)
        self.analog_sig_source_x_0.set_frequency(self.signal_freq_1 - self.signal_freq)

    def get_signal_freq_2(self):
        return self.signal_freq_2

    def set_signal_freq_2(self, signal_freq_2):
        self.signal_freq_2 = signal_freq_2
        self.analog_sig_source_x_0_1.set_frequency(self.signal_freq_2 - self.signal_freq)

    def get_signal_freq_1(self):
        return self.signal_freq_1

    def set_signal_freq_1(self, signal_freq_1):
        self.signal_freq_1 = signal_freq_1
        self.analog_sig_source_x_0.set_frequency(self.signal_freq_1 - self.signal_freq)

    def get_signal_freq_0(self):
        return self.signal_freq_0

    def set_signal_freq_0(self, signal_freq_0):
        self.signal_freq_0 = signal_freq_0
        self.analog_sig_source_x_0_0.set_frequency(self.signal_freq_0 - self.signal_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtl_source.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(self.signal_freq, self.samp_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)


def main(top_block_cls=am_audio_decoder_1, options=None):

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
