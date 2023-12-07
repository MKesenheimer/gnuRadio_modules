/* -*- c++ -*- */
/*
 * Copyright 2023 Matthias Kesenheimer.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_MANCHESTER_DECODE_MANCHESTER_DECODE_H
#define INCLUDED_MANCHESTER_DECODE_MANCHESTER_DECODE_H

#include <gnuradio/manchester_decode/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace manchester_decode {

    /*!
     * \brief <+description of block+>
     * \ingroup manchester_decode
     *
     */
    template <class T>
    class MANCHESTER_DECODE_API manchester_decode : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<manchester_decode<T>> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of manchester_decode::manchester_decode.
       *
       * To avoid accidental use of raw pointers, manchester_decode::manchester_decode's
       * constructor is in a private implementation
       * class. manchester_decode::manchester_decode::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t samples_per_symbol = 4, size_t nsync_symbols = 0, int bit_mode = 0, int endianess = 0);
    };

    typedef manchester_decode<std::uint8_t> manchester_decode_b;
    typedef manchester_decode<std::int16_t> manchester_decode_s;
    typedef manchester_decode<std::int32_t> manchester_decode_i;
    typedef manchester_decode<float> manchester_decode_f;

  } // namespace manchester_decode
} // namespace gr

#endif /* INCLUDED_MANCHESTER_DECODE_MANCHESTER_DECODE_H */
