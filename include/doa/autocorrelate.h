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


#ifndef INCLUDED_DOA_AUTOCORRELATE_H
#define INCLUDED_DOA_AUTOCORRELATE_H

#include <doa/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace doa {

    /*!
     * \brief Determine the correlation matrix of the inputs across antenna elements. 
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
      typedef boost::shared_ptr<autocorrelate> sptr;

      /*!
       * \brief Make an autocorrelate block.
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
