/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_FIND_LOCAL_MAX_IMPL_H
#define INCLUDED_DOA_FIND_LOCAL_MAX_IMPL_H

#include <gnuradio/doa/find_local_max.h>
#include <armadillo>
#include <functional>

using namespace arma;

namespace gr {
    namespace doa {

        class find_local_max_impl : public find_local_max
        {
        private:
            const int d_num_max_vals; 
            const int d_vector_len;
            const float d_x_min;
            const float d_x_max;
            fvec d_x_axis;      

        public:
            find_local_max_impl(int num_max_vals, int vector_len, float x_min, float x_max);
            ~find_local_max_impl();

            // Where all the action really happens
            int work(int noutput_items,
                    gr_vector_const_void_star& input_items,
                    gr_vector_void_star& output_items);
            static void find_one_local_peak_indx(uvec &pk_indx, const fvec in_vec, const int d_num_max_vals)
            {
                pk_indx = index_max(in_vec);
            }
            static void find_more_than_one_local_peak_indxs(uvec &pk_indxs, const fvec in_vec, const int d_num_max_vals);   
            void (*find_local_peak_indxs)(uvec &pk_indxs, const fvec in_vec, const int d_num_max_vals);    

        };

    } // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_FIND_LOCAL_MAX_IMPL_H */
