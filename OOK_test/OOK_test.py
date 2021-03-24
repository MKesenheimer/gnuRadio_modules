#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: kesenheimer
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from OOKDemodulator import OOKDemodulator  # grc-generated hier_block
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation

from gnuradio import qtgui

class OOK_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
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

        self.settings = Qt.QSettings("GNU Radio", "OOK_test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e5
        self.samp_per_symbol = samp_per_symbol = 600
        self.freq_0 = freq_0 = 20e3
        self.data = data = (1,1,1,1,1,1,1,1,1,0, 1, 0,1,1,0,0,1,0)

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_sink_x_1 = qtgui.sink_f(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_1_win)
        self.blocks_vector_source_x_0 = blocks.vector_source_c(data, True, 1, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, 600)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/Users/kesenheimer/Documents/Basteln/SDR/OOK_test/OOK_test.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_0, 1, 0, 0)
        self.OOKDemodulator_1 = OOKDemodulator(
            freq_0=freq_0,
            gain=2,
            low_pass_cutoff=5000,
            offset=0.5,
            samp_per_sym=600,
            samp_rate=samp_rate,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.OOKDemodulator_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.OOKDemodulator_1, 1), (self.qtgui_sink_x_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.OOKDemodulator_1, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_repeat_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "OOK_test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.OOKDemodulator_1.set_samp_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate)

    def get_samp_per_symbol(self):
        return self.samp_per_symbol

    def set_samp_per_symbol(self, samp_per_symbol):
        self.samp_per_symbol = samp_per_symbol

    def get_freq_0(self):
        return self.freq_0

    def set_freq_0(self, freq_0):
        self.freq_0 = freq_0
        self.OOKDemodulator_1.set_freq_0(self.freq_0)
        self.analog_sig_source_x_0.set_frequency(self.freq_0)

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
        self.blocks_vector_source_x_0.set_data(self.data, [])





def main(top_block_cls=OOK_test, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
