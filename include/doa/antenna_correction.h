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


#ifndef INCLUDED_DOA_ANTENNA_CORRECTION_H
#define INCLUDED_DOA_ANTENNA_CORRECTION_H

#include <doa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace doa {

    /*!
     * \brief Performs a scaling operation on a correlation matrix.
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
      typedef boost::shared_ptr<antenna_correction> sptr;

      /*!
       * \brief Make a block to correct a correlation matrix for non-uniform antenna gain and phase. 
       *
       * \param num_ant_ele     Number of antenna elements
       * \param config_filename Config file consisting of antenna calibration values
       */
      static sptr make(int num_ant_ele, char* config_filename);
    };

  } // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_ANTENNA_CORRECTION_H */

