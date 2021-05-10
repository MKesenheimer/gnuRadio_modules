#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-extract_payload author.
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
import extract_payload_swig as extract_payload

class qa_extract_payload(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        self.samp_rate = samp_rate = 32000
        src_data =        (1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0)
        bitpattern =      (1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        epa = extract_payload.extract_payload(bitpattern, len(expected_result), len(bitpattern))
        src = blocks.vector_source_b(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_char*1, samp_rate, True)
        self.tb.connect((thr, 0), (epa, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((epa, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(expected_result, result_data)

    def test_002_t(self):
        self.samp_rate = samp_rate = 32000
        src_data =        (0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0,0,0,0,0,0,0)
        bitpattern =      (1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0)
        epa = extract_payload.extract_payload(bitpattern, len(expected_result), len(bitpattern))
        src = blocks.vector_source_b(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_char*1, samp_rate, True)
        self.tb.connect((thr, 0), (epa, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((epa, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(expected_result, result_data)

    def test_003_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,0,0,0,0,0,0,0, # 0
                    0,0,0,0,1,0,1,0, # 8 
                    1,0,1,0,1,0,1,1, # 16
                    1,1,1,1,1,1,1,0, # 24
                    1,1,1,0,1,1,1,0, # 32
                    1,1,0,0,0,0,0,0, # 40
                    0,0,0,0,0,0,0,0, # 48
                    0,0,0,0,0,1,0,1, # 56
                    0,1,0,1,0,1,0,1, # 64
                    1,1,1,1,1,1,1,1, # 72
                    0,1,1,1,0,1,1,1, # 80
                    0,1,1,0,0,0,0,0, # 88
                    0,0)             # 96
        bitpattern = (1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0,0,1,1,1,0,1,1,1,0,1,1,0)
        epa = extract_payload.extract_payload(bitpattern, len(expected_result) / 2, len(bitpattern))
        src = blocks.vector_source_b(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_char*1, samp_rate, True)
        self.tb.connect((thr, 0), (epa, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((epa, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(expected_result, result_data)

    def test_004_t(self):
        self.samp_rate = samp_rate = 32000
        src_data = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        bitpattern = (1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1)
        expected_result = (0,1,1,1,0,1,1,1,0,1,1,0,0,1,1,1,0,1,1,1,0,1,1,0)
        epa = extract_payload.extract_payload(bitpattern, len(expected_result) / 2, 4)
        src = blocks.vector_source_b(src_data, False, 1, [])
        snk = blocks.vector_sink_b(1, 0)
        thr = blocks.throttle(gr.sizeof_char*1, samp_rate, True)
        self.tb.connect((thr, 0), (epa, 0))
        self.tb.connect((src, 0), (thr, 0))
        self.tb.connect((epa, 0), (snk, 0))
        self.tb.run()
        result_data = snk.data()
        #print(result_data)
        self.assertEqual(expected_result, result_data)

if __name__ == '__main__':
    gr_unittest.run(qa_extract_payload)
