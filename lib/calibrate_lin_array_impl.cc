/* -*- c++ -*- */
/* 
 * Copyright 2016 
 * Srikanth Pagadarai <srikanth.pagadarai@gmail.com>
 * Travis F. Collins <travisfcollins@gmail.com>
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "calibrate_lin_array_impl.h"

#define COPY_MEM false  // Do not copy matrices into separate memory
#define FIX_SIZE true   // Keep dimensions of matrices constant

namespace gr {
  namespace doa {

    calibrate_lin_array::sptr
    calibrate_lin_array::make(float norm_spacing, int num_ant_ele, float pilot_angle)
    {
      return gnuradio::get_initial_sptr
        (new calibrate_lin_array_impl(norm_spacing, num_ant_ele, pilot_angle));
    }

    /*
     * The private constructor
     */
    calibrate_lin_array_impl::calibrate_lin_array_impl(float norm_spacing, int num_ant_ele, float pilot_angle)
      : gr::sync_block("calibrate_lin_array",
              gr::io_signature::make(1, 1, num_ant_ele*num_ant_ele*sizeof(gr_complex)),
              gr::io_signature::make(1, 1, num_ant_ele*sizeof(gr_complex))),
	      d_norm_spacing(norm_spacing),
	      d_num_ant_ele(num_ant_ele),	      
	      d_pilot_angle(pilot_angle)
    {

	// form antenna array locations centered around zero and normalize
        d_array_loc = fcolvec(d_num_ant_ele, fill::zeros);
        for (int nn = 0; nn < d_num_ant_ele; nn++)
        {
            d_array_loc(nn) = d_norm_spacing*0.5*(d_num_ant_ele-1-2*nn);
        }
	
        // form array response matrix
        cx_fcolvec v_temp(d_num_ant_ele, fill::zeros);
        d_diagmat_v_vec = cx_fmat(d_num_ant_ele, d_num_ant_ele);
        d_diagmat_v_vec_conj = cx_fmat(d_num_ant_ele, d_num_ant_ele);

        // generate array manifold vector for pilot angle
        amv(v_temp, d_array_loc, datum::pi*d_pilot_angle/180.0);
        d_diagmat_v_vec = diagmat(v_temp);
        // save transposed copy
        d_diagmat_v_vec_conj = diagmat(conj(v_temp));

    }

    /*
     * Our virtual destructor.
     */
    calibrate_lin_array_impl::~calibrate_lin_array_impl()
    {
    }

    // array manifold vector generating function
    void calibrate_lin_array_impl::amv(cx_fcolvec& v_ii, fcolvec& array_loc, float theta)
    {
        // sqrt(-1)
        const gr_complex i = gr_complex(0.0, 1.0);
	// array manifold vector
    	v_ii = exp(i*(-1.0*2*datum::pi*cos(theta)*array_loc));
    }

    /*
     * This approach is based on 
     * V. C. Soon, L. Tong, Y. F. Huang and R. Liu, 
     * "A Subspace Method for Estimating Sensor Gains and Phases," 
     * in IEEE Transactions on Signal Processing, 
     * vol. 42, no. 4, pp. 973-976, Apr 1994.
     */
    int
    calibrate_lin_array_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];      

      // process each input vector (Rxx matrix)
      fvec eig_val, W_eig_val;
      cx_fmat eig_vec, W_eig_vec;      
      cx_fmat U_S, U_S_sq;
      cx_fmat W;
      for (int item = 0; item < noutput_items; item++)
      {
          // make input pointer into matrix pointer
          cx_fmat in_matrix(in+item*d_num_ant_ele*d_num_ant_ele, d_num_ant_ele, d_num_ant_ele);
          cx_fvec gain_phase_est_vec(out+item*d_num_ant_ele, d_num_ant_ele, COPY_MEM, FIX_SIZE);          

          // determine EVD of the auto-correlation matrix
          eig_sym(eig_val, eig_vec, in_matrix);

          // signal subspace column vector corresponding to one pilot source and its square matrix
          cx_fmat U_S = eig_vec.col(d_num_ant_ele-1);
          cx_fmat U_S_sq = U_S*trans(U_S);

	  // array gain and phase vector is the eigenvector of W that corresponds to eigenvalue of unity
          W = d_diagmat_v_vec_conj*U_S_sq*d_diagmat_v_vec;
          eig_sym(W_eig_val, W_eig_vec, W);	  

	  gain_phase_est_vec = W_eig_vec.col(d_num_ant_ele-1);
	  
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace doa */
} /* namespace gr */

