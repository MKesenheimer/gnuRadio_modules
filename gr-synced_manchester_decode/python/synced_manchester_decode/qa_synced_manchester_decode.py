#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Matthias Kesenheimer.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import random
try:
    from gnuradio.synced_manchester_decode import *
except ImportError:
    import os
    import sys
    dirname, filename = os.path.split(os.path.abspath(__file__))
    sys.path.append(os.path.join(dirname, "bindings"))
    from gnuradio.synced_manchester_decode import *

class qa_synced_manchester_decode(gr_unittest.TestCase):

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
        mdecode = synced_manchester_decode_f(samples_per_symbol, 0, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a manchester stream with multiple samples per symbol, with noise
    def test_002_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = int(len(src_data) / len(expected_result))
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_f(samples_per_symbol, 0, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    def test_003_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = 8
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_f(samples_per_symbol, 0, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

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
        mdecode = synced_manchester_decode_f(samples_per_symbol, 0, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

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
        mdecode = synced_manchester_decode_f(samples_per_symbol, 0, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

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
        mdecode = synced_manchester_decode_f(samples_per_symbol, 0, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # stream starts with garbage and then synchronization header
    def test_007_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = 8
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_f(samples_per_symbol, 0, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # stream starts with garbage and then synchronization header
    def test_008_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = 8
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_f(samples_per_symbol, 0, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # samples per symbol not given, it is calculated with the initialization sequence at the beginning
    def test_009_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0)
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_f(1, 8, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # samples per symbol not given, it is calculated with the initialization sequence at the beginning
    # stream starts with garbage and then synchronization header
    def test_010_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0)
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_f(1, 8, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # samples per symbol not given, it is calculated with the initialization sequence at the beginning
    # stream starts with garbage and then synchronization header
    # stream with two parts of data, divided by ones
    def test_011_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0)
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_f(1, 8, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # samples per symbol not given, it is calculated with the initialization sequence at the beginning
    # stream starts with garbage and then synchronization header
    # stream with two parts of data, divided by zeros
    def test_012_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0)
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_f(1, 8, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # samples per symbol not given, it is calculated with the initialization sequence at the beginning
    # stream starts with garbage and then synchronization header
    # stream with two parts of data, divided by ones
    def test_013_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0)
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_f(1, 8, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a manchester stream with multiple samples per symbol, but samples per symbol vary
    # samples per symbol not given, it is calculated with the initialization sequence at the beginning
    # stream starts with garbage and then synchronization header
    # stream with two parts of data, divided by ones
    def test_014_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1)
        src_data = [(s - 0.5 + (random.random() - 0.5) * 0.1) for s in src_data] # add some noise and bring to [-0.5, 0.5]
        #print(src_data)
        expected_result = (0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0)
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_f(1, 8, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a perfect manchester stream (with float inputs)
    def test_float_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,0,1)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = int(len(src_data) / len(expected_result))
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_f(samples_per_symbol, 0, 0, 0)
        src = blocks.vector_source_f(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a perfect manchester stream (with int inputs)
    def test_int_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,0,1)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = int(len(src_data) / len(expected_result))
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_i(samples_per_symbol, 0, 0, 0)
        src = blocks.vector_source_i(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_int*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a perfect manchester stream (with short inputs)
    def test_short_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,0,1)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = int(len(src_data) / len(expected_result))
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_s(samples_per_symbol, 0, 0, 0)
        src = blocks.vector_source_s(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_short*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

    # decoding a perfect manchester stream (with byte inputs)
    def test_byte_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,0,1)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = int(len(src_data) / len(expected_result))
        #print(samples_per_symbol)
        mdecode = synced_manchester_decode_b(samples_per_symbol, 0, 0, 0)
        src = blocks.vector_source_b(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.tb.connect((thr, 0), (mdecode, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((mdecode, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(list(expected_result), result_data)

if __name__ == '__main__':
    gr_unittest.run(qa_synced_manchester_decode)
