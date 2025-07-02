/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_CALIBRATE_LIN_ARRAY_H
#define INCLUDED_DOA_CALIBRATE_LIN_ARRAY_H

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
 * as input and generates a complex vector of size (number of antenna elements x 1) 
 * which can be utilized to calibrate a linear array. 
 */
class DOA_API calibrate_lin_array : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<calibrate_lin_array> sptr;

    /*!
       * \brief Make a block to calibrate linear arrays.
       *
       * \param norm_spacing    Normalized spacing between antenna elements
       * \param num_ant_ele     Number of antenna elements
       * \param pilot_angle     Known angle of a pilot transmitter used for calibration
       */
      static sptr make(float norm_spacing, int num_ant_ele, float pilot_angle);
};

} // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_CALIBRATE_LIN_ARRAY_H */
