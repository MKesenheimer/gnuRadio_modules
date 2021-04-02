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

#ifndef INCLUDED_FIND_MAX_CHANNEL_FIND_MAX_CHANNEL_IMPL_H
#define INCLUDED_FIND_MAX_CHANNEL_FIND_MAX_CHANNEL_IMPL_H

#include <find_max_channel/find_max_channel.h>

//#define DEBUG

namespace gr {
  namespace find_max_channel {

    class find_max_channel_impl : public find_max_channel {
     private:
      const size_t m_vec_length;
      const float m_threshold;
      float m_last_max_channel;
#ifdef DEBUG
      size_t m_counter;
#endif

     public:
      find_max_channel_impl(size_t vec_length, float threshold);
      ~find_max_channel_impl();

      // Where all the action really happens
      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace find_max_channel
} // namespace gr

#endif /* INCLUDED_FIND_MAX_CHANNEL_FIND_MAX_CHANNEL_IMPL_H */

