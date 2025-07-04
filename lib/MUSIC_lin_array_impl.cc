/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "MUSIC_lin_array_impl.h"
#include <gnuradio/io_signature.h>

#define COPY_MEM false  // Do not copy matrices into separate memory
#define FIX_SIZE true   // Keep dimensions of matrices constant

namespace gr {
    namespace doa {

        using input_type = gr_complex;  
        using output_type = float;

        MUSIC_lin_array::sptr
        MUSIC_lin_array::make(float norm_spacing, int num_targets, int inputs, int pspectrum_len)
        {
            return gnuradio::make_block_sptr<MUSIC_lin_array_impl>(norm_spacing, num_targets, inputs, pspectrum_len);
        }


        /*
        * The private constructor
        */
        MUSIC_lin_array_impl::MUSIC_lin_array_impl(float norm_spacing, int num_targets, int inputs, int pspectrum_len)
            : gr::sync_block("MUSIC_lin_array",
                    gr::io_signature::make(1, 1, sizeof(input_type)*inputs*inputs),
                    gr::io_signature::make(1, 1, sizeof(output_type)*pspectrum_len)),
                d_norm_spacing(norm_spacing),
                d_num_targets(num_targets),
                d_num_ant_ele(inputs),
                d_pspectrum_len(pspectrum_len)
        {
            // form antenna array locations centered around zero and normalize
            d_array_loc = fcolvec(d_num_ant_ele, fill::zeros);
            for (int nn = 0; nn < d_num_ant_ele; nn++)
            {
                d_array_loc(nn) = d_norm_spacing*0.5*(d_num_ant_ele-1-2*nn);
            }
        
            // form theta vector
            d_theta = new float[d_pspectrum_len];
            d_theta[0] = 0.0;
            float theta_prev = 0.0, theta;
            for (int ii = 1; ii < d_pspectrum_len; ii++)
            {
            theta = theta_prev+180.0/d_pspectrum_len;
        theta_prev = theta;
            d_theta[ii] = datum::pi*theta/180.0;
            }

            // form array response matrix
            cx_fcolvec vii_temp(d_num_ant_ele, fill::zeros);
            d_vii_matrix = cx_fmat(d_num_ant_ele,d_pspectrum_len);
            d_vii_matrix_trans = cx_fmat(d_pspectrum_len,d_num_ant_ele);
            for (int ii = 0; ii < d_pspectrum_len; ii++)
            {
            // generate array manifold vector for each theta
            amv(vii_temp, d_array_loc, d_theta[ii]);
            // add as column to matrix
            d_vii_matrix.col(ii) = vii_temp;
            }
            // save transposed copy
            d_vii_matrix_trans = trans(d_vii_matrix);
        }

        /*
        * Our virtual destructor.
        */
        MUSIC_lin_array_impl::~MUSIC_lin_array_impl() 
        {
        }

        // array manifold vector generating function
        void MUSIC_lin_array_impl::amv(cx_fcolvec& v_ii, fcolvec& array_loc, float theta)
        {
            // sqrt(-1)
            const gr_complex i = gr_complex(0.0, 1.0);
        // array manifold vector
            v_ii = exp(i*(-1.0*2*datum::pi*cos(theta)*array_loc));
        }


        int MUSIC_lin_array_impl::work(int noutput_items,
                                    gr_vector_const_void_star& input_items,
                                    gr_vector_void_star& output_items)
        {
            const input_type *in = (const input_type *) input_items[0];
            output_type *out = (output_type *) output_items[0];  

            // process each input vector (Rxx matrix)
            fvec eig_val;
            cx_fmat eig_vec;
            cx_fmat U_N;
            cx_fmat U_N_sq;
            for (int item = 0; item < noutput_items; item++)
            {
                // make input pointer into matrix pointer
                cx_fmat in_matrix(in+item*d_num_ant_ele*d_num_ant_ele, d_num_ant_ele, d_num_ant_ele);
                fvec out_vec(out+item*d_pspectrum_len, d_pspectrum_len, COPY_MEM, FIX_SIZE);

                // determine EVD of the auto-correlation matrix
                eig_sym(eig_val, eig_vec, in_matrix);

                // noise subspace and its square matrix
                U_N = eig_vec.cols(0, d_num_ant_ele-d_num_targets-1);
                U_N_sq = U_N*trans(U_N);

                // determine pseudo-spectrum for each value of theta in [0.0, 180.0)
                gr_complex Q_temp;
                for (int ii = 0; ii < d_pspectrum_len; ii++)
                {
                    Q_temp = as_scalar(d_vii_matrix_trans.row(ii)*U_N_sq*d_vii_matrix.col(ii));
                    out_vec(ii) = 1.0/Q_temp.real();
                }
                out_vec = 10.0*log10(out_vec/out_vec.max());  
            }
            
            return noutput_items;
        }
    } /* namespace doa */
} /* namespace gr */
