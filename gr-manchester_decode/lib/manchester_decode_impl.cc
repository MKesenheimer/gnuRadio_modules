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

    template <class T>
    typename manchester_decode<T>::sptr manchester_decode<T>::make() {
        return gnuradio::make_block_sptr<manchester_decode_impl<T>>();
    }

    /*
     * The private constructor
     */
    template <class T>
    manchester_decode_impl<T>::manchester_decode_impl()
      : gr::block("manchester_decode",
                gr::io_signature::make(1, 1, sizeof(T)),
                gr::io_signature::make(1, 1, sizeof(uint8_t))) {
        const int alignment_multiple = volk_get_alignment() / sizeof(uint8_t);
#ifdef DEBUG
        GR_LOG_INFO(d_logger, boost::format("alignment_multiple = %d") % alignment_multiple);
#endif
        // Constrains buffers to work on a set item alignment
        this->set_alignment(std::max(1, alignment_multiple));
        // Constrain the noutput_items argument passed to forecast and general_work
        //this->set_output_multiple(multiple);
        // Set the approximate output rate / input rate as an integer ratio
        this->set_relative_rate(1, (uint64_t)m_samples_per_symbol); // interpolation, decimation
    }

    template <class T>
    void manchester_decode_impl<T>::forecast(int noutput_items, gr_vector_int &ninput_items_required) {
#ifdef DEBUG
        GR_LOG_INFO(d_logger, boost::format("noutput_items = %d") % noutput_items);
#endif
        ninput_items_required[0] = (int)(noutput_items / m_samples_per_symbol);
    }

    template <class T>
    int manchester_decode_impl<T>::general_work (int noutput_items,
            gr_vector_int &ninput_items,
            gr_vector_const_void_star &input_items,
            gr_vector_void_star &output_items) {
        const T* in = reinterpret_cast<const T*>(input_items[0]);
        uint8_t* out = reinterpret_cast<uint8_t*>(output_items[0]);
        const size_t nsamples = ninput_items[0];
        size_t out_count = 0;

#ifdef DEBUG
        GR_LOG_INFO(d_logger, boost::format("---- new work ----"));
        GR_LOG_INFO(d_logger, boost::format("ninput_items = %d, noutput_items = %d") % nsamples % noutput_items);
#endif  

        // set the output vector
        auto set_out = [&](int v) {
            out[out_count++] = v;
        };

        // observe falling or rising edge and set output accordingly
        auto observe_edge = [&](uint8_t first, uint8_t second) { 
            if (!first && second) {
                set_out(0);
            } else if (first && !second) {
                set_out(1);
            }
        };

        for (size_t i = 0; i < nsamples - 1; i+=2) {
            observe_edge(in[i], in[i+1]);
        }

#ifdef DEBUG
        for (int i = 0; i < nsamples; ++i)
            GR_LOG_INFO(d_logger, boost::format("out = %x") % (int)out[i]);
#endif

        this->consume(0, nsamples);

#ifdef DEBUG
        GR_LOG_INFO(d_logger, boost::format("---- end work ----\n"));
#endif

        noutput_items = out_count;
        return noutput_items;
    }

    template class manchester_decode<std::uint8_t>;
    template class manchester_decode<std::int16_t>;
    template class manchester_decode<std::int32_t>;
    template class manchester_decode<float>;
  } /* namespace manchester_decode */
} /* namespace gr */
