# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT doa_sources)
    message(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT doa_sources)

########################################################################
# Check for pygccxml
########################################################################
gr_python_check_module_raw("pygccxml" "import pygccxml" PYGCCXML_FOUND)

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND doa_python_files python_bindings.cc)

gr_pybind_make_oot(doa ../../.. gr::doa "${doa_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(
    TARGET doa_python
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:doa_python>
            ${PROJECT_BINARY_DIR}/test_modules/gnuradio/doa/)

install(
    TARGETS doa_python
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/doa
    COMPONENT pythonapi)
