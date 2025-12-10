/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_POWER_DETECTION_CPP_H
#define INCLUDED_DOA_POWER_DETECTION_CPP_H

#include <gnuradio/doa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
namespace doa {

/*!
 * \brief Power detection block with buffer capture and replay
 * \ingroup doa
 *
 * Detects signal power on the first input channel. When power exceeds
 * threshold, captures signal to buffer. During silence, replays captured signal.
 */
class DOA_API power_detection_cpp : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<power_detection_cpp> sptr;

    /*!
     * \brief Create a power detection block
     * \param num_inputs Number of input channels
     * \param sample_rate Sample rate in Hz
     * \param threshold Power threshold for detection
     * \param buffer_size Size of capture/playback buffer in samples
     */
    static sptr make(int num_inputs, double sample_rate, float threshold, int buffer_size = 1024);
};

} // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_POWER_DETECTION_CPP_H */
