/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DOA_POWER_DETECTION_CPP_IMPL_H
#define INCLUDED_DOA_POWER_DETECTION_CPP_IMPL_H

#include <gnuradio/doa/power_detection_cpp.h>
#include <vector>

namespace gr {
namespace doa {

class power_detection_cpp_impl : public power_detection_cpp
{
private:
    int d_num_inputs;
    double d_sample_rate;
    float d_threshold;
    int d_buffer_size;
    int d_averaging_window;
    
    // Dual buffer system for capture and playback
    std::vector<std::vector<gr_complex>> d_capture_buffer;   // [channel][sample]
    std::vector<std::vector<gr_complex>> d_playback_buffer;  // [channel][sample]
    
    std::vector<float> d_power_buffer;
    
    int d_capture_index;
    int d_playback_index;
    int d_power_buffer_index;
    
    bool d_capturing;
    bool d_playback_buffer_valid;
    bool d_buffer_fill_complete;
    
    float d_power_sum;

    void validate_and_promote_buffer();

public:
    power_detection_cpp_impl(int num_inputs, double sample_rate, float threshold, int buffer_size);
    ~power_detection_cpp_impl();

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_POWER_DETECTION_CPP_IMPL_H */
