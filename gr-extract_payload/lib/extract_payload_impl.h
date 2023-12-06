/* -*- c++ -*- */
/*
 * Copyright 2023 Matthias Kesenheimer.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_EXTRACT_PAYLOAD_EXTRACT_PAYLOAD_IMPL_H
#define INCLUDED_EXTRACT_PAYLOAD_EXTRACT_PAYLOAD_IMPL_H

#include <gnuradio/extract_payload/extract_payload.h>

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
      const bool m_prependHeader;
      const std::string m_lengthTagKey;
      size_t m_navailable;

     public:
      extract_payload_impl(const std::vector<uint8_t>& bitpattern, unsigned int payloadLength, unsigned int headerLength, bool prependHeader, const std::string& lengthTagKey);
      ~extract_payload_impl();

      // Where all the action really happens
      void forecast(int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace extract_payload
} // namespace gr

#endif /* INCLUDED_EXTRACT_PAYLOAD_EXTRACT_PAYLOAD_IMPL_H */
