/* -*- c++ -*- */
/*
 * Copyright 2021 gr-extract_payload author.
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

#ifndef INCLUDED_EXTRACT_PAYLOAD_EXTRACT_PAYLOAD_IMPL_H
#define INCLUDED_EXTRACT_PAYLOAD_EXTRACT_PAYLOAD_IMPL_H

#include <extract_payload/extract_payload.h>

//#define DEBUG

namespace gr {
  namespace extract_payload {

    class extract_payload_impl : public extract_payload
    {
     private:
      const std::vector<uint8_t> m_bitpattern;
      const unsigned int m_payloadLength;
      const unsigned int m_headerLength;
      const unsigned int m_bits_or_bytes = 0;
      const unsigned int m_endianess = 0;
      size_t m_navailable;

     public:
      extract_payload_impl(const std::vector<uint8_t>& bitpattern, unsigned int payloadLength, unsigned int headerLength);
      ~extract_payload_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace extract_payload
} // namespace gr

#endif /* INCLUDED_EXTRACT_PAYLOAD_EXTRACT_PAYLOAD_IMPL_H */

