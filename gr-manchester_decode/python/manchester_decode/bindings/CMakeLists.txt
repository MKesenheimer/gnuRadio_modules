# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT manchester_decode_sources)
    message(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT manchester_decode_sources)

########################################################################
# Check for pygccxml
########################################################################
gr_python_check_module_raw("pygccxml" "import pygccxml" PYGCCXML_FOUND)

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND manchester_decode_python_files
    manchester_decode_python.cc python_bindings.cc)

gr_pybind_make_oot(manchester_decode ../../.. gr::manchester_decode "${manchester_decode_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(
    TARGET manchester_decode_python
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:manchester_decode_python>
            ${PROJECT_BINARY_DIR}/test_modules/gnuradio/manchester_decode/)

install(
    TARGETS manchester_decode_python
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/manchester_decode
    COMPONENT pythonapi)
