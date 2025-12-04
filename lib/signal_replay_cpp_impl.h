/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_SIGNAL_REPLAY_CPP_IMPL_H
#define INCLUDED_DOA_SIGNAL_REPLAY_CPP_IMPL_H

#include <gnuradio/doa/signal_replay_cpp.h>
#include <vector>

namespace gr {
namespace doa {

class signal_replay_cpp_impl : public signal_replay_cpp
{
private:
    std::vector<gr_complex> d_signal_data;
    size_t d_position;
    bool d_repeat;
    int d_interpolation;
    std::string d_filename;

    bool load_numpy_file(const std::string& filename);

public:
    signal_replay_cpp_impl(const std::string& filename, bool repeat, int interpolation);
    ~signal_replay_cpp_impl();

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_SIGNAL_REPLAY_CPP_IMPL_H */
