#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-set_variable author.
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


import pmt
import numpy
from gnuradio import gr

class set_variable(gr.sync_block):
    """
    This block will take an input and allow you to set a gnuradio variable.
    """
    def __init__(self, callback):
        gr.sync_block.__init__(self,
            name="set_variable",
            in_sig=[numpy.float32],
            out_sig=[numpy.float32])
        
        self.callback = callback
        self.new_val = 0

    def work(self, input_items, output_items):
        in0 = input_items[0]
        try:
            #gr.log.info("---- input items ----")
            #gr.log.info("number of inputs = {}".format(len(input_items)))
            for i in range(len(in0)):
                #gr.log.info("{}".format(in0[i]))
                if in0[i] != self.new_val: #in0[i] > 0 and
                    output_items[0][i] = 1
                    self.new_val = in0[i]
                    #gr.log.info("new value ({}) = {}".format(i, self.new_val))
                    self.callback(self.new_val)
            #gr.log.info("---- end work ----")
        except Exception as e:
            gr.log.error("Error with input conversion: {}".format(e))

        return len(output_items[0])

    def stop(self):
        return True