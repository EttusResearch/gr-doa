/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 * Travis F. Collins <travisfcollins@gmail.com>
 * Srikanth Pagadarai <srikanth.pagadarai@gmail.com>
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


#include "autocorrelate_impl.h"
#include <gnuradio/io_signature.h>
#include <armadillo>

#define COPY_MEM false  // Do not copy matrices into separate memory
#define FIX_SIZE true   // Keep dimensions of matrices constant

namespace gr {
    namespace doa {

        using input_type = gr_complex;
        using output_type = gr_complex;

        autocorrelate::sptr
        autocorrelate::make(int inputs, int snapshot_size, int overlap_size, int avg_method)
        {
            return gnuradio::make_block_sptr<autocorrelate_impl>(inputs, snapshot_size, overlap_size, avg_method);
        }

        /*
        * The private constructor
        */
        autocorrelate_impl::autocorrelate_impl(int inputs, int snapshot_size, int overlap_size, int avg_method)
            : gr::block("autocorrelate",
                    gr::io_signature::make(inputs, inputs, sizeof(input_type)),
                    gr::io_signature::make(1, 1, sizeof(output_type)*inputs*inputs)),
            d_num_inputs(inputs),
            d_snapshot_size(snapshot_size),
            d_overlap_size(overlap_size),
            d_avg_method(avg_method)
        {
            d_nonoverlap_size = d_snapshot_size-d_overlap_size;
            set_history(d_overlap_size+1);

            // Create container for temporary matrix
            d_input_matrix = arma::cx_fmat(snapshot_size,inputs);

            // initialize the reflection matrix
            d_J.eye(d_num_inputs, d_num_inputs);
            d_J = fliplr(d_J);
        }

        /*
        * Our virtual destructor.
        */
        autocorrelate_impl::~autocorrelate_impl() 
        {
        }

        void autocorrelate_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
        {
            for (size_t i=0; i < ninput_items_required.size(); i++)
                ninput_items_required[i] = d_nonoverlap_size*noutput_items;
        }

        int autocorrelate_impl::general_work(int output_matrices,
                                            gr_vector_int &ninput_items,
                                            gr_vector_const_void_star &input_items,
                                            gr_vector_void_star &output_items)
        {
            //auto in = static_cast<const input_type*>(input_items[0]);
            //auto out = static_cast<output_type*>(output_items[0]);

            // Cast pointer
            gr_complex *out = (gr_complex *) output_items[0];

            // Create each output matrix
            for (int i=0; i < output_matrices; i++)
            {
                // Form input matrix
                for(int k=0; k < d_num_inputs; k++) 
                {
                    const gr_complex* in_ptr = static_cast<const gr_complex*>(input_items[k]);
                    memcpy((void*)d_input_matrix.colptr(k),
                    &in_ptr[i*d_nonoverlap_size],
                    sizeof(gr_complex)*d_snapshot_size);
                }
                
                // Make output pointer into matrix pointer
                arma::cx_fmat out_matrix(out+d_num_inputs*d_num_inputs*i,d_num_inputs,d_num_inputs,COPY_MEM,FIX_SIZE);

                // Do autocorrelation
                out_matrix = (1.0/d_snapshot_size)*d_input_matrix.st()*conj(d_input_matrix);
                if (d_avg_method == 1) {
                    out_matrix = 0.5*out_matrix+(0.5/d_snapshot_size)*d_J*conj(out_matrix)*d_J;
                }
            }
            // Tell runtime system how many input items we consumed on
            // each input stream.
            consume_each (d_nonoverlap_size * output_matrices);			

            // Tell runtime system how many output items we produced.
            return output_matrices;
        }
    } /* namespace doa */
} /* namespace gr */
