/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_ANTENNA_CORRECTION_IMPL_H
#define INCLUDED_DOA_ANTENNA_CORRECTION_IMPL_H

#include <gnuradio/doa/antenna_correction.h>
#include <armadillo>
using namespace arma;

namespace gr {
    namespace doa {

        class antenna_correction_impl : public antenna_correction
        {
            private:
                cx_fcolvec d_ComplexGain;
                const int d_num_ant_ele;

            public:
                antenna_correction_impl(int num_ant_ele, const std::string& config_filename);
                ~antenna_correction_impl();

                // Where all the action really happens
                int work(int noutput_items,
                        gr_vector_const_void_star& input_items,
                        gr_vector_void_star& output_items);
        };
    } // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_ANTENNA_CORRECTION_IMPL_H */
