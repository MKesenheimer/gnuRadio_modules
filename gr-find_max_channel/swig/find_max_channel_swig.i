/* -*- c++ -*- */

#define FIND_MAX_CHANNEL_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "find_max_channel_swig_doc.i"

%{
#include "find_max_channel/find_max_channel.h"
%}

%include "find_max_channel/find_max_channel.h"
GR_SWIG_BLOCK_MAGIC2(find_max_channel, find_max_channel);
