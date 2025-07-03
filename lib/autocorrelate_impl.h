/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_AUTOCORRELATE_IMPL_H
#define INCLUDED_DOA_AUTOCORRELATE_IMPL_H

#include <gnuradio/doa/autocorrelate.h>
#include <armadillo>

namespace gr {
    namespace doa {

    class autocorrelate_impl : public autocorrelate
    {
    private:
        const int d_num_inputs;
        const int d_snapshot_size;
        const int d_overlap_size;
        const int d_avg_method; // value assigned using the initialization list of the constructor
        int d_nonoverlap_size;
        arma::cx_fmat d_J;
        arma::cx_fmat d_input_matrix;

    public:
        autocorrelate_impl(int inputs, int snapshot_size, int overlap_size, int avg_method);
        ~autocorrelate_impl();

        // Where all the action really happens
        void forecast(int noutput_items, gr_vector_int& ninput_items_required);

        int general_work(int noutput_items,
                        gr_vector_int& ninput_items,
                        gr_vector_const_void_star& input_items,
                        gr_vector_void_star& output_items);
    };

    } // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_AUTOCORRELATE_IMPL_H */
