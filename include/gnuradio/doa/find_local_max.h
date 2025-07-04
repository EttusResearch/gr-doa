/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_FIND_LOCAL_MAX_H
#define INCLUDED_DOA_FIND_LOCAL_MAX_H

#include <gnuradio/doa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
    namespace doa {
        /*!
        * \brief <+description of block+>
        * \ingroup doa
        *
        * \details
        * This block takes a vector of size (vector-length x 1) 
        * as input and outputs a float vector of size (number of max. values x 1)
        * consisting of max. values and a float vector of size (number of max. values x 1)
        * consisting of their locations.
        */
        class DOA_API find_local_max : virtual public gr::sync_block
        {
        public:
            typedef std::shared_ptr<find_local_max> sptr;

            /*!
            * \brief Return a shared_ptr to a new instance of doa::find_local_max.
            *
            * \param num_max_vals    Number of max. values
            * \param vector_len      Length of the input vector
            * \param x_min           Min. value of the index vector
            * \param x_max           Max. value of the index vector
            */
            static sptr make(int num_max_vals, int vector_len, float x_min, float x_max);
        };
    } // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_FIND_LOCAL_MAX_H */
