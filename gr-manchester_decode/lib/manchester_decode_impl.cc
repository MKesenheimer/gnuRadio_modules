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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <volk/volk.h>
#include "manchester_decode_impl.h"

namespace gr {
  namespace manchester_decode {

    manchester_decode::sptr
    manchester_decode::make(size_t samples_per_symbol, size_t message_length, 
      int bit_mode, int endianess, int nsync_symbols) {
      return gnuradio::get_initial_sptr
        (new manchester_decode_impl(samples_per_symbol, message_length, bit_mode, endianess, nsync_symbols));
    }


    /*
     * The private constructor
     */
    manchester_decode_impl::manchester_decode_impl(size_t samples_per_symbol, size_t message_length, 
      int bit_mode, int endianess, int nsync_symbols)
      : gr::block("manchester_decode",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(uint8_t))),
              m_samples_per_symbol(samples_per_symbol),
              m_bits_or_bytes(bit_mode),
              m_endianess(endianess),
              m_nsync_symbols(nsync_symbols)
#ifdef V2
              , m_tick(0), 
              m_mode(0),
              m_last(0), 
              m_lasttrans(0),
              m_nextbit(0),
              m_message_length(message_length),
              m_nextsmp(0),
              m_msgoffset(0)
#endif
    {
      const int alignment_multiple = volk_get_alignment() / sizeof(uint8_t);
#ifdef DEBUG
      GR_LOG_INFO(d_logger, boost::format("alignment_multiple = %d") % alignment_multiple);
#endif
      // Constrains buffers to work on a set item alignment
      this->set_alignment(std::max(1, alignment_multiple));
      // Constrain the noutput_items argument passed to forecast and general_work
      //this->set_output_multiple(multiple);
      // Set the approximate output rate / input rate as an integer ratio

#ifdef V1
      this->set_relative_rate(1, (uint64_t)samples_per_symbol); // interpolation, decimation
#endif

#ifdef V2
      this->set_relative_rate((uint64_t)m_message_length, (uint64_t)samples_per_symbol); // interpolation, decimation
      m_bytes = new uint8_t[m_message_length];
#endif
    }

    /*
     * Our virtual destructor.
     */
    manchester_decode_impl::~manchester_decode_impl() {
#ifdef V2
      delete[] m_bytes;
#endif
    }

    void manchester_decode_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required) {
#ifdef DEBUG
      GR_LOG_INFO(d_logger, boost::format("noutput_items = %d") % noutput_items);
#endif

#ifdef V1
      ninput_items_required[0] = (int)(noutput_items / m_samples_per_symbol);
#endif

#ifdef V2
      ninput_items_required[0] = (int)(m_message_length * noutput_items);
#endif
    }

    int manchester_decode_impl::general_work(int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items) {
      const float* in = reinterpret_cast<const float*>(input_items[0]);
      uint8_t* out = reinterpret_cast<uint8_t*>(output_items[0]);
      const size_t nsamples = ninput_items[0];

#ifdef DEBUG
      GR_LOG_INFO(d_logger, boost::format("---- new work ----"));
      GR_LOG_INFO(d_logger, boost::format("ninput_items = %d, noutput_items = %d") % nsamples % noutput_items);
#endif

#ifdef V1
      size_t out_count = 0;
      size_t sample_count = 0;
      uint8_t last_sample = in[0] >=0 ? 1 : 0;
      uint8_t symbol[] = {0, 0};
      size_t symbol_count = 0;
      size_t total_sample_count = 0;
      size_t total_symbol_count = 0;
      bool start = false;
      for (size_t i = 0; i <= nsamples; ++i) {
        uint8_t sample = 0;
        if (i < nsamples)
          if (in[i] >= 0) sample = 1;

        // start when first rising edge is detected
        if (!start && sample == 1 && last_sample == 0) {
          sample_count = m_samples_per_symbol / 2;
          start = true;
        }

        if (start) {
          if (sample != last_sample || i == nsamples) {
            // set the output vector
            auto set_out = [&](int v) {
              if (m_bits_or_bytes == 0) {
                out[out_count++] = v;
              } else {
                if (m_endianess == 0) {
                  out[(int)(out_count/8)] |= v << (7 - out_count % 8); // little endian
                } else {
                  out[(int)(out_count/8)] |= v << (out_count % 8); // big endian
                }
                out_count++;
              }
            };

            // observe falling or rising edge and set output accordingly
            auto observe_edge = [&](uint8_t first, uint8_t second) { 
              if (!first && second) {
                set_out(0);
              } else if (first && !second) {
                set_out(1);
              }
              symbol_count = 0;
            };

            // count the number of equal samples and compare the
            // symbols when there was a change
            float ratio = (float) 2 * sample_count / m_samples_per_symbol;
            if (ratio >= 0.5 && ratio < 1.5) {
              symbol[symbol_count++] = last_sample;
              if (symbol_count >= 2)
                observe_edge(symbol[0], symbol[1]);
            } else if (ratio >= 1.5 && ratio < 2.5) {
              symbol[symbol_count++] = last_sample;
              observe_edge(symbol[0], symbol[1]);
              symbol[symbol_count++] = last_sample;
            }

            // if it is the beginning of the transmition, determine the samples_per_symbol
            if (total_symbol_count <= m_nsync_symbols) {
              total_sample_count += sample_count;
              total_symbol_count++;
            }

            // new symbol next run, reset sample count
            sample_count = 0;
          }

          sample_count++;
        } // if (start)

        /*if (total_symbol_count < 10) {
          m_samples_per_symbol = (int)(2 * total_sample_count / total_symbol_count);
        }*/

        last_sample = sample;
      }

#ifdef DEBUG
      if (total_symbol_count != 0) {
        GR_LOG_INFO(d_logger, boost::format("samples_per_symbol = %d") % (int)(2 * total_sample_count / total_symbol_count));
        GR_LOG_INFO(d_logger, boost::format("m_samples_per_symbol = %d") % (int)(m_samples_per_symbol));
      }
#endif

      if (m_bits_or_bytes == 0) {
        noutput_items = out_count;
      } else {
        noutput_items = (int) (out_count / 8);
      }
#endif

#ifdef V2
      for (int smp = 0; smp < nsamples; ++smp) {
        int i = m_tick;
        int v = (int)in[smp];
        // unsynced
        if (m_mode == 0) {
          // high to low
          if (v == 0 && m_last == 1) {
            int delay = i - m_lasttrans;
            // valid period
            if (delay >= 8 && delay <= 10) {
              m_syncstart = m_lasttrans;
              m_synccount = 1;
              m_mode = 1;
            }
            m_lasttrans = i;
          }
        // sync started
        } else if (m_mode == 1) {
          // high to low
          if (v == 0 && m_last == 1) {
            int delay = i - m_lasttrans;
            // valid period
            if (delay >= 7 && delay <= 11) {
              m_synccount++;
            } else {
              m_mode = 0;
            }
            m_lasttrans = i;
          } else {
            // lost sync
            if (i - m_lasttrans >= 13) {
              m_mode = 0;
              // success
              if (m_synccount >= 200) {
                m_mode = 2;
                m_nextbit = 0;
                m_period = (m_lasttrans - m_syncstart) / m_synccount;
                for (int j = 0; j < m_message_length; ++j) {
                  m_bytes[j] = 0;
                }
                m_nextsmp = (int) (m_lasttrans - m_period / 4 + (m_nextbit + 3 + 8 + m_msgoffset) * m_period / 2);
                // Error
                if (m_nextsmp <= i) {
                  GR_LOG_WARN(d_logger, "Bad Offset - cannot go that far back");
                  m_mode = 0;
                }
              }
            }
          }
        } else if (m_mode == 2) {
          if (i == m_nextsmp) {
            m_bytes[(int)(m_nextbit/8)] |= v << (7 - m_nextbit % 8); // little endian (?)
            //m_bytes[(int)(m_nextbit/8)] |= v << (m_nextbit % 8); // big endian
            m_nextbit++;
            m_nextsmp = (int)(m_lasttrans - m_period / 4 + (m_nextbit + 3 + 8 + m_msgoffset) * m_period / 2);
            // done
            if (m_nextbit >= 8 * m_message_length) {
              m_mode = 0;
              for (int j = 0; j <= m_message_length; ++j) {
                out[j] = m_bytes[j]; // TODO: memcopy
              }
            }
          }
        }
        m_last = v;
        m_tick++;
      }

      noutput_items = m_message_length;
#endif

#ifdef DEBUG
      for (int i = 0; i < count; ++i)
        GR_LOG_INFO(d_logger, boost::format("out = %x") % (int)out[i]);
#endif

      this->consume(0, nsamples);

#ifdef DEBUG
      GR_LOG_INFO(d_logger, boost::format("---- end work ----\n"));
#endif

      return noutput_items;
    }

  } /* namespace manchester_decode */
} /* namespace gr */

