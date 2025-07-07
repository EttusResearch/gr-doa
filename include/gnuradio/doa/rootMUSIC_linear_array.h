/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_ROOTMUSIC_LINEAR_ARRAY_H
#define INCLUDED_DOA_ROOTMUSIC_LINEAR_ARRAY_H

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
 * as input and generates a complex vector of size (pseudo-spectrum length x 1) 
 * whose arg-max values represent the estimated DoAs. 
 */
class DOA_API rootMUSIC_linear_array : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<rootMUSIC_linear_array> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of doa::rootMUSIC_linear_array.
     *
     * \param norm_spacing    Normalized spacing between antenna elements
     * \param num_targets     Known number of targets 
     * \param num_ant_ele     Number of antenna elements
     */
    static sptr make(float norm_spacing, int num_targets, int num_ant_ele);
};

} // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_ROOTMUSIC_LINEAR_ARRAY_H */
