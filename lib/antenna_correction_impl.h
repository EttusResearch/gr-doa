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

#ifndef INCLUDED_DOA_ANTENNA_CORRECTION_IMPL_H
#define INCLUDED_DOA_ANTENNA_CORRECTION_IMPL_H

#include <doa/antenna_correction.h>

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
      antenna_correction_impl(int num_ant_ele, char* config_filename);
      ~antenna_correction_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_ANTENNA_CORRECTION_IMPL_H */
