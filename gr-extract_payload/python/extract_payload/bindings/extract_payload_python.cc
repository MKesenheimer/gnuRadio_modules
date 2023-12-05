/*
 * Copyright 2023 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(extract_payload.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(fd8c1cfe588e5b31ddf17ad789411ccb)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/extract_payload/extract_payload.h>
// pydoc.h is automatically generated in the build directory
#include <extract_payload_pydoc.h>

void bind_extract_payload(py::module& m)
{

    using extract_payload    = gr::extract_payload::extract_payload;


    py::class_<extract_payload, gr::block, gr::basic_block,
        std::shared_ptr<extract_payload>>(m, "extract_payload", D(extract_payload))

        .def(py::init(&extract_payload::make),
           D(extract_payload,make)
        )
        



        ;




}








