/* -*- c++ -*- */
/*
 * Copyright 2023 Matthias Kesenheimer.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_EXTRACT_PAYLOAD_EXTRACT_PAYLOAD_H
#define INCLUDED_EXTRACT_PAYLOAD_EXTRACT_PAYLOAD_H

#include <gnuradio/extract_payload/api.h>
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
      typedef std::shared_ptr<extract_payload> sptr;

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
