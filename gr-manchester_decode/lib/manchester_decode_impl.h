/* -*- c++ -*- */
/*
 * Copyright 2023 Matthias Kesenheimer.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_MANCHESTER_DECODE_MANCHESTER_DECODE_IMPL_H
#define INCLUDED_MANCHESTER_DECODE_MANCHESTER_DECODE_IMPL_H

#include <gnuradio/manchester_decode/manchester_decode.h>

namespace gr {
  namespace manchester_decode {

    template <class T>
    class manchester_decode_impl : public manchester_decode<T>
    {
     private:
      const size_t m_samples_per_symbol = 2;

     public:
      manchester_decode_impl();

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
