/* -*- c++ -*- */
/*
 * Copyright 2023 Matthias Kesenheimer.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include <volk/volk.h>
#include "manchester_decode_impl.h"

namespace gr {
  namespace manchester_decode {

    manchester_decode::sptr
    manchester_decode::make(size_t samples_per_symbol, size_t n_sync_symbols, int bit_mode, int endianess) {
      return gnuradio::make_block_sptr<manchester_decode_impl>(
        samples_per_symbol, n_sync_symbols, bit_mode, endianess);
    }


    /*
     * The private constructor
     */
    manchester_decode_impl::manchester_decode_impl(size_t samples_per_symbol, size_t nsync_symbols, int bit_mode, int endianess)
      : gr::block("manchester_decode",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(uint8_t))),
              m_samples_per_symbol(samples_per_symbol),
              m_nsync_symbols(nsync_symbols),
              m_bits_or_bytes(bit_mode),
              m_endianess(endianess) {
      const int alignment_multiple = volk_get_alignment() / sizeof(uint8_t);
#ifdef DEBUG
      GR_LOG_INFO(d_logger, boost::format("alignment_multiple = %d") % alignment_multiple);
#endif
      // Constrains buffers to work on a set item alignment
      this->set_alignment(std::max(1, alignment_multiple));
      // Constrain the noutput_items argument passed to forecast and general_work
      //this->set_output_multiple(multiple);
      // Set the approximate output rate / input rate as an integer ratio
      this->set_relative_rate(1, (uint64_t)samples_per_symbol); // interpolation, decimation
    }

    /*
     * Our virtual destructor.
     */
    manchester_decode_impl::~manchester_decode_impl() {}

    void
    manchester_decode_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required) {
#ifdef DEBUG
      GR_LOG_INFO(d_logger, boost::format("noutput_items = %d") % noutput_items);
#endif
      ninput_items_required[0] = (int)(noutput_items / m_samples_per_symbol);
    }

    int
    manchester_decode_impl::general_work (int noutput_items,
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

      size_t out_count = 0;
      size_t sample_count = 0;
      uint8_t last_sample = in[0] >= 0 ? 1 : 0;
      uint8_t symbol[] = {0, 0}; // TODO: make static
      // the first rising edge is always a zero -> start at symbol_count = 1
      size_t symbol_count = 1; // TODO: make static
      size_t total_sample_count = 0;
      size_t total_symbol_count = 0;
      bool start = false;
      bool synced = false;
      for (size_t i = 0; i <= nsamples; ++i) {
        uint8_t sample = 0;
        if (i < nsamples)
          if (in[i] >= 0) sample = 1;

        // start when first rising edge is detected
        if (!start && sample == 1 && last_sample == 0) start = true;

        if (start) {
          // rising or falling edge
          if (sample != last_sample || i == nsamples) {
            // if it is the beginning of the transmition, determine the samples_per_symbol
            if (sample_count > 0 && total_symbol_count < m_nsync_symbols) {
              total_sample_count += sample_count;
              total_symbol_count++;
            }
            
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

            // new symbol next run, reset sample count
            sample_count = 0;
          } // (sample != last_sample || i == nsamples)

          // syncing finished, calculate the samples per symbol
          if (!synced && total_symbol_count > 0 && total_symbol_count == m_nsync_symbols) {
            m_samples_per_symbol = (int)(2 * total_sample_count / total_symbol_count);
            //GR_LOG_INFO(d_logger, boost::format("set samples_per_symbol = %d") % m_samples_per_symbol);
            this->set_relative_rate(1, (uint64_t)m_samples_per_symbol);
            synced = true;
          }

          sample_count++;

          // if no edge for a longer period -> reset
          if (synced && sample_count >= 3 * m_samples_per_symbol) {
            start = false;
            synced = false;
            total_sample_count = 0;
            total_symbol_count = 0;
            symbol[0] = 0;
            symbol_count = 1;
            sample_count = 0;
            if (m_bits_or_bytes != 0) {
              out_count += 8 - (out_count % 8);
            }
          }
        } // if (start)

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

#ifdef DEBUG
      for (int i = 0; i < nsamples; ++i)
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
