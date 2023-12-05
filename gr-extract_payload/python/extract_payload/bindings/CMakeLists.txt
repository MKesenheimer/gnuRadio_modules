# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT extract_payload_sources)
    message(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT extract_payload_sources)

########################################################################
# Check for pygccxml
########################################################################
gr_python_check_module_raw("pygccxml" "import pygccxml" PYGCCXML_FOUND)

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND extract_payload_python_files
    extract_payload_python.cc python_bindings.cc)

gr_pybind_make_oot(extract_payload ../../.. gr::extract_payload "${extract_payload_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(
    TARGET extract_payload_python
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:extract_payload_python>
            ${PROJECT_BINARY_DIR}/test_modules/gnuradio/extract_payload/)

install(
    TARGETS extract_payload_python
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/extract_payload
    COMPONENT pythonapi)
