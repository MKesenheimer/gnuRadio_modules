/* -*- c++ -*- */
/*
 * Copyright 2021 gr-find_max_channel author.
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
#include "find_max_channel_impl.h"

namespace gr {
  namespace find_max_channel {

    find_max_channel::sptr
    find_max_channel::make(size_t vec_length, float threshold) {
      return gnuradio::get_initial_sptr
        (new find_max_channel_impl(vec_length, threshold));
    }


    /*
     * The private constructor
     */
    find_max_channel_impl::find_max_channel_impl(size_t vec_length, float threshold)
      : gr::sync_decimator("find_max_channel",
              gr::io_signature::make(1, 1, vec_length * sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(float)), 1),
        m_vec_length(vec_length),
        m_threshold(threshold),
        m_last_max_channel(0)
#ifdef DEBUG
        , m_counter(0)
#endif
    {
      //this->set_relative_rate(1, (uint64_t)vec_length);
      this->set_relative_rate(1, 1);
    }

    /*
     * The virtual destructor.
     */
    find_max_channel_impl::~find_max_channel_impl() {}

    int find_max_channel_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items) {
      //const size_t ninput_items = input_signature()->sizeof_stream_item(0) / sizeof(float);
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];

      size_t size = noutput_items;

      while (size-- > 0) {
        *out = 0;
        float max = *in;
        for (int j = 1; j < m_vec_length; ++j) {
          in++;
          if (*in > max) {
            *out = j;
            max = *in;
          }
        }

        if (m_threshold != -999 && max >= m_threshold) {
          m_last_max_channel = *out;
        } else {
          *out = m_last_max_channel;
        }

        out++;

#ifdef DEBUG
        if ((m_counter++) % 100 == 0) {
          GR_LOG_INFO(d_logger, boost::format("noutput_items=%d") % noutput_items);
          GR_LOG_INFO(d_logger, boost::format("channel=%d, max=%d, m_last_max_channel=%d") 
            % out[0] % max % m_last_max_channel);
        }
#endif
      }

      return noutput_items;
    }
  } /* namespace find_max_channel */
} /* namespace gr */

