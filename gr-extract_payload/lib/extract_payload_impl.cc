/* -*- c++ -*- */
/*
 * Copyright 2023 Matthias Kesenheimer.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include <volk/volk.h>
#include <algorithm>
#include <stdio.h>
#include "extract_payload_impl.h"

namespace gr {
  namespace extract_payload {

    extract_payload::sptr
    extract_payload::make(const std::vector<uint8_t>& bitpattern, unsigned int payloadLength, unsigned int headerLength)
    {
      return gnuradio::make_block_sptr<extract_payload_impl>(
        bitpattern, payloadLength, headerLength);
    }


    /*
     * The private constructor
     */
    extract_payload_impl::extract_payload_impl(const std::vector<uint8_t>& bitpattern, unsigned int payloadLength, unsigned int headerLength)
      : gr::block("extract_payload",
            gr::io_signature::make(1, 1, sizeof(uint8_t)),
            gr::io_signature::make(1, 1, sizeof(uint8_t))),
        m_bitpattern(bitpattern),
        m_payloadLength(payloadLength),
        m_headerLength(headerLength),
        m_navailable(0)
    {
        const int alignment_multiple = volk_get_alignment() / sizeof(uint8_t);
#ifdef DEBUG
        GR_LOG_INFO(d_logger, boost::format("alignment_multiple = %d") % alignment_multiple);
#endif
        // Constrains buffers to work on a set item alignment
        this->set_alignment(std::max(1, alignment_multiple));
        // Constrain the noutput_items argument passed to forecast and general_work
        this->set_output_multiple(m_headerLength + m_payloadLength);
        // Set the approximate output rate / input rate as an integer ratio
        //this->set_relative_rate(1, 1);
        this->set_relative_rate((uint64_t)m_payloadLength, (uint64_t)m_headerLength + m_payloadLength); // interpolation, decimation
    }

    /*
     * Our virtual destructor.
     */
    extract_payload_impl::~extract_payload_impl() {}

    void
    extract_payload_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required) {
        int n = (int)((m_payloadLength) * noutput_items / (m_headerLength + m_payloadLength));
        ninput_items_required[0] = n > 1? n : 1;
        //ninput_items_required[0] = 1;
        //ninput_items_required[0] = n;
        //ninput_items_required[0] = noutput_items;
#ifdef DEBUG
        GR_LOG_INFO(d_logger, boost::format("noutput_items = %d, ninput_items_required = %d") % noutput_items % ninput_items_required[0]);
#endif
    }

    int
    extract_payload_impl::general_work (int noutput_items, gr_vector_int &ninput_items, gr_vector_const_void_star &input_items, gr_vector_void_star &output_items) {
        const uint8_t *in = (const uint8_t *) input_items[0];
        uint8_t* out = reinterpret_cast<uint8_t*>(output_items[0]);
        const size_t nsamples = ninput_items[0];

#ifdef DEBUG
        GR_LOG_INFO(d_logger, boost::format("---- new work ----"));
        GR_LOG_INFO(d_logger, boost::format("ninput_items = %d, noutput_items = %d") % nsamples % noutput_items);
#endif

        size_t out_count = 0;
        size_t start = 0;
        using Iter = std::vector<uint8_t>::const_iterator;
        std::vector<uint8_t> vin(in, in + nsamples);

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

        // if the payload is distributed over several buffers, process the next symbols until the full payload is processed
        while (m_navailable > 0 && start < nsamples) {
            set_out(vin[start]);
            start++;
            m_navailable--;
        }

        while (start < nsamples) {
            Iter it = std::search(vin.begin() + start, vin.end(), m_bitpattern.begin(), m_bitpattern.end());
            if (std::distance<Iter>(it, vin.end()) >= m_bitpattern.size()) {
                it += m_bitpattern.size();
                m_navailable = m_payloadLength;
                for (Iter i = it; i != vin.end() && i != it + m_payloadLength; ++i) {
                    m_navailable--;
                    set_out(*i);
                }
                start = std::distance<Iter>(vin.begin(), it) + out_count;
#ifdef DEBUG
                GR_LOG_INFO(d_logger, boost::format("start = %d") % start);
#endif
            }
        
            if (it == vin.end()) break;
        }

#if 0
        if (out_count > 0) {
            //std::cout << boost::format("ninput_items = %d") % nsamples << std::endl;
            //std::cout << "out = ";
            std::vector<uint8_t> vout;
            vout.resize((int)out_count/8 + 1);
            for (int i = 0; i < out_count; ++i)
                vout[(int)(i/8)] |= out[i] << (7 - i % 8); // TODO: does not work if payload is divided over multiple buffers
            for (int i = 0; i < out_count/8; ++i)
                std::cout << boost::format("%02x") % (int)(vout[i]);
        
            if (m_navailable == 0)
                std::cout << std::endl;
        }
#endif


#ifdef DEBUG
        for (int i = 0; i < out_count; ++i)
            GR_LOG_INFO(d_logger, boost::format("out = %x") % (int)out[i]);
#endif

        this->consume(0, nsamples);

#ifdef DEBUG
        GR_LOG_INFO(d_logger, boost::format("---- end work ----\n"));
#endif

        if (m_bits_or_bytes == 0) {
            noutput_items = out_count;
        } else {
            noutput_items = (int) (out_count / 8);
        }

        return noutput_items;
    }

  } /* namespace extract_payload */
} /* namespace gr */
