/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_ROOTMUSIC_LINEAR_ARRAY_IMPL_H
#define INCLUDED_DOA_ROOTMUSIC_LINEAR_ARRAY_IMPL_H

#include <gnuradio/doa/rootMUSIC_linear_array.h>
#include <armadillo>
using namespace arma;

namespace gr {
    namespace doa {

    class rootMUSIC_linear_array_impl : public rootMUSIC_linear_array
    {
        private:
            float d_norm_spacing;
            int d_num_targets;
            int d_num_ant_ele;
            cx_fmat d_comp_mat;

        public:
            rootMUSIC_linear_array_impl(float norm_spacing, int num_targets, int num_ant_ele);
            ~rootMUSIC_linear_array_impl();

            // Where all the action really happens
            int work(int noutput_items,
                    gr_vector_const_void_star& input_items,
                    gr_vector_void_star& output_items);
                    
                void get_roots_polynomial(cx_fmat& A, cx_fcolvec& roots); 
        };

    } // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_ROOTMUSIC_LINEAR_ARRAY_IMPL_H */
