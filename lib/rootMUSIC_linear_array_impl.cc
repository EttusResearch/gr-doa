/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "rootMUSIC_linear_array_impl.h"
#include <gnuradio/io_signature.h>

#define COPY_MEM false  // Do not copy matrices into separate memory
#define FIX_SIZE true   // Keep dimensions of matrices constant

namespace gr {
    namespace doa {

        using input_type = gr_complex;
        using output_type = float;

        rootMUSIC_linear_array::sptr
        rootMUSIC_linear_array::make(float norm_spacing, int num_targets, int num_ant_ele)
        {
            return gnuradio::make_block_sptr<rootMUSIC_linear_array_impl>(norm_spacing, num_targets, num_ant_ele);
        }


        /*
        * The private constructor
        */
        rootMUSIC_linear_array_impl::rootMUSIC_linear_array_impl(float norm_spacing, int num_targets, int num_ant_ele)
            : gr::sync_block("rootMUSIC_linear_array",
                        gr::io_signature::make(1, 1, sizeof(input_type)*num_ant_ele*num_ant_ele),
                        gr::io_signature::make(1, num_targets, num_targets*sizeof(output_type))),
                    d_norm_spacing(norm_spacing),
                    d_num_targets(num_targets),
                    d_num_ant_ele(num_ant_ele)
            {
            // initialization of the Frobenius companion matrix
            d_comp_mat.zeros(2*d_num_ant_ele-2, 2*d_num_ant_ele-2);

            // set the first sub-diagonal to all-ones
            d_comp_mat.diag(-1).ones();
            }

        /*
        * Our virtual destructor.
        */
        rootMUSIC_linear_array_impl::~rootMUSIC_linear_array_impl() 
        {
        }

        void rootMUSIC_linear_array_impl::get_roots_polynomial(cx_fmat& A, cx_fcolvec& roots) 
        {
            cx_fcolvec u(2*d_num_ant_ele-1);

            // determine the polynomial vector and normalize it
            for (int ii = -d_num_ant_ele+1; ii < 0; ii++) 
            {
                u(ii+d_num_ant_ele-1) = sum(A.diag(ii));
                u(d_num_ant_ele-1-ii) = conj(u(ii+d_num_ant_ele-1)); 
            }
            u(d_num_ant_ele-1) = sum(A.diag());
            u = (gr_complex(-1.0, 0.0)/u(2*d_num_ant_ele-2))*u;

            // assign u to the last-column of the Frobenius companion matrix
            d_comp_mat.col(2*d_num_ant_ele-3) = u.rows(0, 2*d_num_ant_ele-3);

            // determine its EVD to get roots of the polynomial vector
            eig_gen(roots, d_comp_mat);     
        }

        int rootMUSIC_linear_array_impl::work(int noutput_items,
                                            gr_vector_const_void_star& input_items,
                                            gr_vector_void_star& output_items)
        {
            const input_type *in = (const input_type *) input_items[0];
            output_type *out = (output_type *) output_items[0];

            // process each input vector (Rxx matrix)
            fcolvec eig_val;
            cx_fmat eig_vec;
            cx_fcolvec eigval_roots, eigval_roots_inside;
            fcolvec dist, dist_inside;
            uvec ind_inside_unit_circle; 
            uword min_dist_index; 

            for (int item = 0; item < noutput_items; item++)
            {
                // make input pointer into matrix pointer
                cx_fmat in_matrix(in+item*d_num_ant_ele*d_num_ant_ele, d_num_ant_ele, d_num_ant_ele);
                fvec out_vec(out+item*d_num_targets, d_num_targets, COPY_MEM, FIX_SIZE);

                // determine EVD of the auto-correlation matrix
                eig_sym(eig_val, eig_vec, in_matrix);

                // noise subspace and its square matrix
                cx_fmat U_N = eig_vec.cols(0, d_num_ant_ele-d_num_targets-1);
                cx_fmat U_N_sq = U_N*trans(U_N);

                // determine the roots of the polynomial generated using U_N_sq
                get_roots_polynomial(U_N_sq, eigval_roots);

                // distance of the roots w.r.t the unit circle
                dist = 1.0-abs(eigval_roots);

                // find roots which are inside the unit circle     
                    ind_inside_unit_circle = find(dist > 0.0);
                eigval_roots_inside = eigval_roots(ind_inside_unit_circle);
                dist_inside = dist(ind_inside_unit_circle);	  

                // of the remaining, find the roots that are closest to the unit circle
                fvec aoa_vec(d_num_targets);
                
                // Check if we have sufficient roots inside the unit circle
                if (dist_inside.n_elem < d_num_targets) {
                    // Not enough roots found inside unit circle, fill with zeros
                    aoa_vec.zeros();
                } else {
                    for (int ii = 0; ii < d_num_targets; ii++) 
                    {
                        min_dist_index = index_min(dist_inside);

                        // locate the root and convert it to correct form
                        aoa_vec(ii) = 180.0*acos(arg(eigval_roots_inside[min_dist_index])/(2*datum::pi*d_norm_spacing))/datum::pi;

                        // discard this minimum to find the next minimum
                        dist_inside(min_dist_index) = datum::inf;
                        eigval_roots_inside(min_dist_index) = gr_complex(datum::inf, 0.0);
                    }
                    
                    // sort the AoA vector only if we have valid values
                    // useful for display purposes
                    aoa_vec = sort(aoa_vec);
                }
                memcpy((char *)&(out[item*d_num_targets]), (const char *)aoa_vec.colptr(0), d_num_targets*sizeof(float));
            }

            // Tell runtime system how many output items we produced.
            return noutput_items;
        }
    } /* namespace doa */
} /* namespace gr */
