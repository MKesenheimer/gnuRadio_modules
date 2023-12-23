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
      static sptr make();
    };




  } // namespace manchester_decode
} // namespace gr

#endif /* INCLUDED_MANCHESTER_DECODE_MANCHESTER_DECODE_H */
