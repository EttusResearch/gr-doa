/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "antenna_correction_impl.h"
#include <gnuradio/io_signature.h>

#include <fstream>

#define COPY_MEM false  // Do not copy matrices into separate memory
#define FIX_SIZE true   // Keep dimensions of matrices constant

namespace gr {
    namespace doa {

        using input_type = gr_complex;
        using output_type = gr_complex;

        antenna_correction::sptr antenna_correction::make(int num_ant_ele, const std::string& config_filename)
        {
            return gnuradio::make_block_sptr<antenna_correction_impl>(num_ant_ele, config_filename);
        }


        /*
        * The private constructor
        */
        antenna_correction_impl::antenna_correction_impl(int num_ant_ele, const std::string& config_filename)
            : gr::sync_block("antenna_correction",
                    gr::io_signature::make(num_ant_ele, num_ant_ele, sizeof(input_type)),
                    gr::io_signature::make(num_ant_ele, num_ant_ele, sizeof(output_type))),
                d_num_ant_ele(num_ant_ele)
        {
            // Read configuration file
            // We assume each line has 2 values gain and phase for a given input
            std::ifstream infile(config_filename);
            // Check exists
            if (!infile.good())
            {
                throw std::invalid_argument("Cannot find configuration file.");
            }
                
            // Do checks as we import gains
            float GainEst, PhaseEst;
            d_ComplexGain = cx_fcolvec(d_num_ant_ele, fill::zeros);
            int i = 0;
            while (infile >> GainEst >> PhaseEst)
            {
                if (i>=d_num_ant_ele) 
                {
                    throw std::invalid_argument("Configuration file has too many inputs.");
                }
                d_ComplexGain(i) = gr_complex(1.0/GainEst, 0)*exp(gr_complex(0,-PhaseEst));
                i++;
            }
            if (i!=d_num_ant_ele){
                throw std::invalid_argument("Configuration file does not have enough inputs.");	
            }
        }
            
        /*
        * Our virtual destructor.
        */
        antenna_correction_impl::~antenna_correction_impl() 
        {
        }

        int antenna_correction_impl::work(int noutput_items,
                                        gr_vector_const_void_star& input_items,
                                        gr_vector_void_star& output_items)
        {
        for(int k=0; k<d_num_ant_ele; k++)
            {
                const gr_complex *in_k = (const gr_complex*) input_items[k];
                gr_complex *out_k = (gr_complex*) output_items[k];
                for (int i=0; i < noutput_items; i++)
                    out_k[i] = d_ComplexGain(k)*in_k[i];		  
            }
            
            // Tell runtime system how many output items we produced.
            return noutput_items;
        }
    } /* namespace doa */
} /* namespace gr */
