/* -*- c++ -*- */

#define DOA_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "doa_swig_doc.i"

%{
#include "doa/autocorrelate.h"
#include "doa/MUSIC_lin_array.h"
#include "doa/rootMUSIC_linear_array.h"
#include "doa/antenna_correction.h"
#include "doa/find_local_max.h"
#include "doa/calibrate_lin_array.h"
%}


%include "doa/autocorrelate.h"
GR_SWIG_BLOCK_MAGIC2(doa, autocorrelate);
%include "doa/MUSIC_lin_array.h"
GR_SWIG_BLOCK_MAGIC2(doa, MUSIC_lin_array);

%include "doa/rootMUSIC_linear_array.h"
GR_SWIG_BLOCK_MAGIC2(doa, rootMUSIC_linear_array);

%include "doa/antenna_correction.h"
GR_SWIG_BLOCK_MAGIC2(doa, antenna_correction);

%include "doa/find_local_max.h"
GR_SWIG_BLOCK_MAGIC2(doa, find_local_max);
%include "doa/calibrate_lin_array.h"
GR_SWIG_BLOCK_MAGIC2(doa, calibrate_lin_array);




