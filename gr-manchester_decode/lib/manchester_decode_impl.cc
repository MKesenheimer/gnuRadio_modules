/* -*- c++ -*- */
/*
 * Copyright 2021 gr-manchester_decode author.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "manchester_decode_impl.h"

namespace gr {
  namespace manchester_decode {

    manchester_decode::sptr
    manchester_decode::make(size_t channel, size_t messageLength, float sampleRate)
    {
      return gnuradio::get_initial_sptr
        (new manchester_decode_impl(channel, messageLength, sampleRate));
    }


    /*
     * The private constructor
     */
    manchester_decode_impl::manchester_decode_impl(size_t channel, size_t messageLength, float sampleRate)
      : gr::sync_decimator("manchester_decode",
              gr::io_signature::make(<+MIN_IN+>, <+MAX_IN+>, sizeof(<+ITYPE+>)),
              gr::io_signature::make(<+MIN_OUT+>, <+MAX_OUT+>, sizeof(<+OTYPE+>)), <+decimation+>)
    {}

    /*
     * Our virtual destructor.
     */
    manchester_decode_impl::~manchester_decode_impl()
    {
    }

    int
    manchester_decode_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const <+ITYPE+> *in = (const <+ITYPE+> *) input_items[0];
      <+OTYPE+> *out = (<+OTYPE+> *) output_items[0];

      // Do <+signal processing+>

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace manchester_decode */
} /* namespace gr */

