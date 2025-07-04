/*
 * Copyright 2025 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */
#include "pydoc_macros.h"
#define D(...) DOC(gr, doa, __VA_ARGS__)
/*
  This file contains docstrings for the Python bindings.
  Do not edit! These were automatically extracted during the binding process
  and will be overwritten during the build process
 */



 static const char *__doc_gr_doa_MUSIC_lin_array = R"doc(
MUSIC Direction of Arrival (DOA) estimator for linear array.

This block implements the MUSIC (MUltiple SIgnal Classification) 
algorithm for DOA estimation using a linear array of antennas.
)doc";


 static const char *__doc_gr_doa_MUSIC_lin_array_MUSIC_lin_array_0 = R"doc(
Constructor for MUSIC linear array DOA estimator.
)doc";


 static const char *__doc_gr_doa_MUSIC_lin_array_make = R"doc(
Make a MUSIC linear array DOA estimator block.

Parameters:
    norm_spacing : Normalized spacing (in wavelengths) between antenna elements
    num_targets : Number of targets to detect
    inputs : Number of input antenna elements
    pspectrum_len : Length of the pseudospectrum output vector
)doc";
