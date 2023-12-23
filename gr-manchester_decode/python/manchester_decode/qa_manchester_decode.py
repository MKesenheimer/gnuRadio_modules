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
    from gnuradio.manchester_decode import *
except ImportError:
    import os
    import sys
    dirname, filename = os.path.split(os.path.abspath(__file__))
    sys.path.append(os.path.join(dirname, "bindings"))
    from gnuradio.manchester_decode import *

class qa_manchester_decode(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    # decoding a perfect manchester stream
    def test_001_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,0,1)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        samples_per_symbol = int(len(src_data) / len(expected_result))
        #print(samples_per_symbol)
        mdecode = manchester_decode_b()
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
    gr_unittest.run(qa_manchester_decode)
