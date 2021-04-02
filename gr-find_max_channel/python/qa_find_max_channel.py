#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-find_max_channel author.
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
import find_max_channel_swig as find_max_channel

class qa_find_max_channel(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    # which is the channel with the maximum value?
    # three values, no threshold
    def test_001_t(self):
        src_data = (0, 1, 2)
        expected_result = (2,) # max value is in the second channel 
        src = blocks.vector_source_f(src_data, False, 3, [])
        mx = find_max_channel.find_max_channel(3) # using no threshold (default)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, mx)
        self.tb.connect(mx, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertEqual(expected_result, result_data)

    # 15 values, no threshold
    def test_002_t(self):
        src_data = (-3, 4, -5.5, 2, 3, 123, 3, 1, 20, 1, 4, -7, 5600, 8, 5)
        expected_result = (12,)
        src = blocks.vector_source_f(src_data, False, 15, [])
        mx = find_max_channel.find_max_channel(15)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, mx)
        self.tb.connect(mx, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertEqual(expected_result, result_data)

    # three times five values, threshold of three
    # 1.) (-3, 4, -5.5, 2, 3) -> gives channel 1
    # 2.) (0, -1, -2, -4, -5) -> would give channel 0, but threshold is three -> take the last value -> 1
    # 3.) (0, 1, 2, 3, 4) -> gives channel 4
    def test_003_t(self):
        src_data = (-3, 4, -5.5, 2, 3, 0, -1, -2, -4, -5, 0, 1, 2, 3, 4)
        expected_result = (1, 1, 4)
        src = blocks.vector_source_f(src_data, False, 5, [])
        mx = find_max_channel.find_max_channel(5, 3)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, mx)
        self.tb.connect(mx, dst)
        self.tb.run()
        result_data = dst.data()
        self.assertEqual(expected_result, result_data)


if __name__ == '__main__':
    gr_unittest.run(qa_find_max_channel)
