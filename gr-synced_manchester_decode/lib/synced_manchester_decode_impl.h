/* -*- c++ -*- */
/*
 * Copyright 2023 Matthias Kesenheimer.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_SYNCED_MANCHESTER_DECODE_SYNCED_MANCHESTER_DECODE_IMPL_H
#define INCLUDED_SYNCED_MANCHESTER_DECODE_SYNCED_MANCHESTER_DECODE_IMPL_H

#include <gnuradio/synced_manchester_decode/synced_manchester_decode.h>

namespace gr {
  namespace synced_manchester_decode {

    template <class T>
    class synced_manchester_decode_impl : public synced_manchester_decode<T>
    {
     private:
      size_t m_samples_per_symbol; // Todo: make static
      const size_t m_nsync_symbols;
      const int m_bits_or_bytes; // 0: bits, 1: bytes
      const int m_endianess; // 0: little endian, 1: big endian

     public:
      synced_manchester_decode_impl(size_t samples_per_symbol, size_t nsync_symbols, int bit_mode, int endianess);

      // Where all the action really happens
      void forecast(int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace synced_manchester_decode
} // namespace gr

#endif /* INCLUDED_SYNCED_MANCHESTER_DECODE_SYNCED_MANCHESTER_DECODE_IMPL_H */
