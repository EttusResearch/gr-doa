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

#ifndef INCLUDED_DOA_FIND_LOCAL_MAX_IMPL_H
#define INCLUDED_DOA_FIND_LOCAL_MAX_IMPL_H

#include <doa/find_local_max.h>
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
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);

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

