/* -*- c++ -*- */
/*
 * Copyright 2021 gr-find_max_channel author.
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

#ifndef INCLUDED_FIND_MAX_CHANNEL_FIND_MAX_CHANNEL_H
#define INCLUDED_FIND_MAX_CHANNEL_FIND_MAX_CHANNEL_H

#include <find_max_channel/api.h>
#include <gnuradio/sync_decimator.h>

namespace gr {
  namespace find_max_channel {

    /*!
     * \brief <+description of block+>
     * \ingroup find_max_channel
     *
     */
    class FIND_MAX_CHANNEL_API find_max_channel : virtual public gr::sync_decimator
    {
     public:
      typedef boost::shared_ptr<find_max_channel> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of find_max_channel::find_max_channel.
       *
       * To avoid accidental use of raw pointers, find_max_channel::find_max_channel's
       * constructor is in a private implementation
       * class. find_max_channel::find_max_channel::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t vec_length = 1024);
    };

  } // namespace find_max_channel
} // namespace gr

#endif /* INCLUDED_FIND_MAX_CHANNEL_FIND_MAX_CHANNEL_H */

