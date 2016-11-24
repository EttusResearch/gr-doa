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
#include "find_local_max_impl.h"
#include <functional>

#define COPY_MEM false  // Do not copy matrices into separate memory
#define FIX_SIZE true   // Keep dimensions of matrices constant

namespace gr {
  namespace doa {

    find_local_max::sptr
    find_local_max::make(int num_max_vals, int vector_len, float x_min, float x_max)
    {
      return gnuradio::get_initial_sptr
        (new find_local_max_impl(num_max_vals, vector_len, x_min, x_max));
    }

    /*
     * The private constructor
     */
    find_local_max_impl::find_local_max_impl(int num_max_vals, int vector_len, float x_min, float x_max)
      : gr::sync_block("find_local_max",
              gr::io_signature::make(1, 1, sizeof(float)*vector_len),
              gr::io_signature::make2(2, 2, num_max_vals*sizeof(float), num_max_vals*sizeof(float))),
	      d_num_max_vals(num_max_vals),
	      d_vector_len(vector_len),
              d_x_min(x_min),
              d_x_max(x_max)
    {
      // determine which find_local_peak_indxs to use
      find_local_peak_indxs = (d_num_max_vals == 1)? find_one_local_peak_indx:find_more_than_one_local_peak_indxs;

      // form x-axis
      d_x_axis.set_size(d_vector_len);
      d_x_axis(0) = d_x_min;
      float x_prev = d_x_min, x;
      float x_range = (d_x_max-d_x_min);
      for (int ii = 1; ii < d_vector_len; ii++)
      {
        x = x_prev+x_range/d_vector_len;
	x_prev = x;
        d_x_axis(ii) = x;
      }

    }

    /*
     * Our virtual destructor.
     */
    find_local_max_impl::~find_local_max_impl()
    {
    }

    void
    find_local_max_impl::find_more_than_one_local_peak_indxs(uvec &pk_indxs, const fvec in_vec, const int d_num_max_vals)
    {
      float peak_ht = -datum::inf;
      uvec indx1 = find(in_vec > peak_ht);
      // sign of first-order difference
      fvec sign_fod_in_vec = sign(diff(in_vec));

      // find flats
      uvec indx_flat = find(sign_fod_in_vec == 0);
      for (int ii=indx_flat.size()-1; ii >=0 ; ii--)
      {
	// back-propagate sign_fod_in_vec for flats
        if ( sign_fod_in_vec( std::min(indx_flat(ii)+1, sign_fod_in_vec.size()-1) ) >= 0 )
	{
            // not a flat peak
	    sign_fod_in_vec(indx_flat(ii)) = 1.0;
	}
	else
        {
            // flat peak
	    sign_fod_in_vec(indx_flat(ii)) = -1.0;
	}
      }

      // finding all peak locations by computing
      // second-order difference of
      // sign of first-order difference
      uvec indx2 = find(diff(sign_fod_in_vec) == -2)+1;

      uvec indx3;
      uvec indx3_unique;
      uvec hist_indx3;
      uvec all_pk_indxs;
      if (!indx2.is_empty())
      {
        // finding set-intersection between indx1 and indx2
        // in order to identify local peaks
	indx3 = join_vert(indx1, indx2);
        indx3_unique = unique(indx3);
        hist_indx3 = hist(indx3, indx3_unique);
        all_pk_indxs = indx1(find(hist_indx3 == 2));
      }

      // peak locations
      fvec all_pks = in_vec(all_pk_indxs);
      fvec all_pks_sorted = sort(all_pks, "descend");
      uvec all_pks_sorted_indx = sort_index(all_pks, "descend");
      unsigned num_valid_peaks = all_pks_sorted_indx.size();
        // Output only peaks we need
        if (num_valid_peaks>=d_num_max_vals)
            pk_indxs = all_pk_indxs(all_pks_sorted_indx.rows(0, d_num_max_vals-1));
        else // Not enough found
        {   unsigned ind = 0;
            uvec max_peak_ind;
            // Grab overall max index if necessary
            if (num_valid_peaks==0)
                find_one_local_peak_indx(max_peak_ind, in_vec, d_num_max_vals);
            else
                max_peak_ind = all_pks_sorted_indx(0);
            // Assign indexes
            while(ind<d_num_max_vals)
            {
                // Use what we have first
                if (ind<num_valid_peaks)
                    pk_indxs(ind) = all_pk_indxs(all_pks_sorted_indx(ind));
                else // Set to first max for unfound peaks
                    pk_indxs(ind) = max_peak_ind(0,0);
                ind++;
            }
        }

    }

    int
    find_local_max_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out1 = (float *) output_items[0];
      float *out2 = (float *) output_items[1];

      // Do <+signal processing+>
      uvec pk_indxs;
      pk_indxs.set_size(d_num_max_vals);
      for (int item = 0; item < noutput_items; item++)
      {
	// make input pointer into vector pointer
        fvec in_vec(in+item*d_vector_len, d_vector_len);
        fvec max_val_vec(out1+item*d_num_max_vals, d_num_max_vals, COPY_MEM, FIX_SIZE);
 	fvec arg_max_vec(out2+item*d_num_max_vals, d_num_max_vals, COPY_MEM, FIX_SIZE);

	find_local_peak_indxs(pk_indxs, in_vec, d_num_max_vals);
	max_val_vec = in_vec(pk_indxs);
	arg_max_vec = sort(d_x_axis(pk_indxs), "descend");

      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace doa */
} /* namespace gr */
