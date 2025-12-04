/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_SIGNAL_REPLAY_CPP_H
#define INCLUDED_DOA_SIGNAL_REPLAY_CPP_H

#include <gnuradio/doa/api.h>
#include <gnuradio/sync_block.h>
#include <string>

namespace gr {
namespace doa {

class DOA_API signal_replay_cpp : virtual public gr::sync_block
{
public:
    typedef std::shared_ptr<signal_replay_cpp> sptr;

    static sptr make(const std::string& filename, bool repeat = true, int interpolation = 1);
};

} // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_SIGNAL_REPLAY_CPP_H */
