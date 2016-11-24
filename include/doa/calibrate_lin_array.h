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


#ifndef INCLUDED_DOA_CALIBRATE_LIN_ARRAY_H
#define INCLUDED_DOA_CALIBRATE_LIN_ARRAY_H

#include <doa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace doa {

    /*!
     * \brief Calibrate a linear antenna array. 
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
      typedef boost::shared_ptr<calibrate_lin_array> sptr;

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

