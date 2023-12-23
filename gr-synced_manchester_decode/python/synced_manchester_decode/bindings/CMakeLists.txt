# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT synced_manchester_decode_sources)
    message(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT synced_manchester_decode_sources)

########################################################################
# Check for pygccxml
########################################################################
gr_python_check_module_raw("pygccxml" "import pygccxml" PYGCCXML_FOUND)

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND synced_manchester_decode_python_files
    synced_manchester_decode_python.cc python_bindings.cc)

gr_pybind_make_oot(synced_manchester_decode ../../.. gr::synced_manchester_decode "${synced_manchester_decode_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(
    TARGET synced_manchester_decode_python
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:synced_manchester_decode_python>
            ${PROJECT_BINARY_DIR}/test_modules/gnuradio/synced_manchester_decode/)

install(
    TARGETS synced_manchester_decode_python
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/synced_manchester_decode
    COMPONENT pythonapi)
