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

#ifndef INCLUDED_DOA_ROOTMUSIC_LINEAR_ARRAY_IMPL_H
#define INCLUDED_DOA_ROOTMUSIC_LINEAR_ARRAY_IMPL_H

#include <doa/rootMUSIC_linear_array.h>
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
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);

      void get_roots_polynomial(cx_fmat& A, cx_fcolvec& roots); 
    };

  } // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_ROOTMUSIC_LINEAR_ARRAY_IMPL_H */

