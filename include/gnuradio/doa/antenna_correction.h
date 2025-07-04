/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_ANTENNA_CORRECTION_H
#define INCLUDED_DOA_ANTENNA_CORRECTION_H

#include <gnuradio/doa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
    namespace doa {

        /*!
        * \brief <+description of block+>
        * \ingroup doa
        *
        * \details
        * This block takes a correlation matrix of size (number of antenna elements x number of antenna elements) 
        * as input and multiplies it with a diagonal matrix of size (number of antenna elements x number of antenna elements) 
        * using calibration values retrieved from a config file. 
        */
        class DOA_API antenna_correction : virtual public gr::sync_block
        {
        public:
            typedef std::shared_ptr<antenna_correction> sptr;

            /*!
            * \brief Return a shared_ptr to a new instance of doa::antenna_correction.
            *
            * \param num_ant_ele     Number of antenna elements
            * \param config_filename Config file consisting of antenna calibration values
            */
            static sptr make(int num_ant_ele, const std::string& config_filename);
        };
    } // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_ANTENNA_CORRECTION_H */
