/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_AUTOCORRELATE_H
#define INCLUDED_DOA_AUTOCORRELATE_H

#include <gnuradio/block.h>
#include <gnuradio/doa/api.h>

namespace gr {
namespace doa {

/*!
 * \brief <+description of block+>
 * \ingroup doa
 *
 * \details
 * This block collects a certain number of samples over each of the input streams
 * and forms a (number of inputs x snap shot size) matrix. Then, it produces 
 * a correlation matrix of size (number of inputs x number of inputs) using 
 * either Forward Averaging method or Forward-Backward Averaging method. 
 */
class DOA_API autocorrelate : virtual public gr::block
{
public:
    typedef std::shared_ptr<autocorrelate> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of doa::autocorrelate.
     *
     * \param inputs          Number of input streams
     * \param snapshot_size   Size of each snapshot
     * \param overlap_size    Size of the overlap between successive snapshots
     * \param avg_method      Use Forward Averaging or Forward-Backward Averaging
     */
    static sptr make(int inputs, int snapshot_size, int overlap_size, int avg_method);
};

} // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_AUTOCORRELATE_H */
