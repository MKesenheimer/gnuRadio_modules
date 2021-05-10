/* -*- c++ -*- */

#define EXTRACT_PAYLOAD_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "extract_payload_swig_doc.i"

%{
#include "extract_payload/extract_payload.h"
%}

%include "extract_payload/extract_payload.h"
GR_SWIG_BLOCK_MAGIC2(extract_payload, extract_payload);
