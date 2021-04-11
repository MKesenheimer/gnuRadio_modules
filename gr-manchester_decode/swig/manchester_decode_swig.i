/* -*- c++ -*- */

#define MANCHESTER_DECODE_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "manchester_decode_swig_doc.i"

%{
#include "manchester_decode/manchester_decode.h"
%}

%include "manchester_decode/manchester_decode.h"
GR_SWIG_BLOCK_MAGIC2(manchester_decode, manchester_decode);
