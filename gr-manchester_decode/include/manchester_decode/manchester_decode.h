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

#ifndef INCLUDED_MANCHESTER_DECODE_MANCHESTER_DECODE_H
#define INCLUDED_MANCHESTER_DECODE_MANCHESTER_DECODE_H

#include <manchester_decode/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace manchester_decode {

    /*!
     * \brief <+description of block+>
     * \ingroup manchester_decode
     */
    class MANCHESTER_DECODE_API manchester_decode : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<manchester_decode> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of manchester_decode::manchester_decode.
       *
       * To avoid accidental use of raw pointers, manchester_decode::manchester_decode's
       * constructor is in a private implementation
       * class. manchester_decode::manchester_decode::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t samples_per_symbol, size_t message_length, int bit_mode = 0, int endianess = 0);
    };

  } // namespace manchester_decode
} // namespace gr

#endif /* INCLUDED_MANCHESTER_DECODE_MANCHESTER_DECODE_H */

