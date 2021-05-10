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

#ifndef INCLUDED_EXTRACT_PAYLOAD_EXTRACT_PAYLOAD_H
#define INCLUDED_EXTRACT_PAYLOAD_EXTRACT_PAYLOAD_H

#include <extract_payload/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace extract_payload {

    /*!
     * \brief <+description of block+>
     * \ingroup extract_payload
     *
     */
    class EXTRACT_PAYLOAD_API extract_payload : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<extract_payload> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of extract_payload::extract_payload.
       *
       * To avoid accidental use of raw pointers, extract_payload::extract_payload's
       * constructor is in a private implementation
       * class. extract_payload::extract_payload::make is the public interface for
       * creating new instances.
       */
      static sptr make(const std::vector<uint8_t>& bitpattern, unsigned int payloadLength, unsigned int headerLength);
    };

  } // namespace extract_payload
} // namespace gr

#endif /* INCLUDED_EXTRACT_PAYLOAD_EXTRACT_PAYLOAD_H */

