#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-manchester_decode author.
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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import manchester_decode_swig as manchester_decode
import random

class qa_manchester_decode(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    # decoding a perfect manchester stream
    def test_001_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,0,1)
        src_data = [(s - 0.5) for s in src_data] # bring to [-0.5, 0.5]
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = int(len(src_data) / len(expected_result))
        #print(samples_per_symbol)
        mdecode = manchester_decode.manchester_decode(samples_per_symbol, 12)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(expected_result, result_data)

    # decoding a manchester stream with multiple samples per symbol, with noise
    def test_002_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = int(len(src_data) / len(expected_result))
        #print(samples_per_symbol)
        mdecode = manchester_decode.manchester_decode(samples_per_symbol, 12)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(expected_result, result_data)
    
    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    def test_003_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = 8
        #print(samples_per_symbol)
        mdecode = manchester_decode.manchester_decode(samples_per_symbol, 12)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(expected_result, result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # stream starts with a bunch of zeros
    def test_004_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = 8
        #print(samples_per_symbol)
        mdecode = manchester_decode.manchester_decode(samples_per_symbol, 12)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(expected_result, result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # stream starts with synchronization header
    def test_005_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = 8
        #print(samples_per_symbol)
        mdecode = manchester_decode.manchester_decode(samples_per_symbol, 12)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(expected_result, result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # stream starts with garbage and then synchronization header
    def test_006_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = 8
        #print(samples_per_symbol)
        mdecode = manchester_decode.manchester_decode(samples_per_symbol, 12)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(expected_result, result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # stream starts with garbage and then synchronization header
    def test_007_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (1,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = 8
        #print(samples_per_symbol)
        mdecode = manchester_decode.manchester_decode(samples_per_symbol, 12)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(expected_result, result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # stream starts with garbage and then synchronization header
    def test_008_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = 8
        #print(samples_per_symbol)
        mdecode = manchester_decode.manchester_decode(samples_per_symbol, 12)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(expected_result, result_data)

if __name__ == '__main__':
    gr_unittest.run(qa_manchester_decode)
