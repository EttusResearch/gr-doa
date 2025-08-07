/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_MUSIC_LIN_ARRAY_H
#define INCLUDED_DOA_MUSIC_LIN_ARRAY_H

#include <gnuradio/doa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
namespace doa {

/*!
 * \brief <+description of block+>
 * \ingroup doa
 *
 */
class DOA_API MUSIC_lin_array : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<MUSIC_lin_array> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of doa::MUSIC_lin_array.
     *
     * \param norm_spacing    Normalized spacing between antenna elements
     * \param num_targets     Known number of targets 
     * \param inputs          Number of input streams (antenna elements)
     * \param pspectrum_len   Length of the Pseudo-Spectrum length
     */
    static sptr make(float norm_spacing, int num_targets, int inputs, int pspectrum_len);
};

} // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_MUSIC_LIN_ARRAY_H */
