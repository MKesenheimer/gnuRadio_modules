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

#ifndef INCLUDED_MANCHESTER_DECODE_MANCHESTER_DECODE_IMPL_H
#define INCLUDED_MANCHESTER_DECODE_MANCHESTER_DECODE_IMPL_H

#include <manchester_decode/manchester_decode.h>

//#define DEBUG
#define V1
//#define V2

namespace gr {
  namespace manchester_decode {

    class manchester_decode_impl : public manchester_decode
    {
     private:
      const size_t m_samples_per_symbol;
      const int m_bits_or_bytes;
      const int m_endianess;

#ifdef V2
      int m_tick;
      int m_mode;
      int m_last;
      int m_lasttrans;
      int m_syncstart;
      int m_synccount;
      int m_nextbit;
      int m_period;
      uint8_t* m_bytes;
      size_t m_message_length;
      int m_nextsmp;
      int m_msgoffset;
#endif

     public:
      manchester_decode_impl(size_t samples_per_symbol, size_t message_length, int bit_mode, int endianess);
      ~manchester_decode_impl();

      // Where all the action really happens
      void forecast(int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace manchester_decode
} // namespace gr

#endif /* INCLUDED_MANCHESTER_DECODE_MANCHESTER_DECODE_IMPL_H */

