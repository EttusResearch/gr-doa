/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "power_detection_cpp_impl.h"
#include <gnuradio/io_signature.h>
#include <cstring>

namespace gr {
namespace doa {

power_detection_cpp::sptr
power_detection_cpp::make(int num_inputs, double sample_rate, float threshold, int buffer_size)
{
    return gnuradio::make_block_sptr<power_detection_cpp_impl>(
        num_inputs, sample_rate, threshold, buffer_size);
}

power_detection_cpp_impl::power_detection_cpp_impl(int num_inputs,
                                                   double sample_rate,
                                                   float threshold,
                                                   int buffer_size)
    : gr::sync_block("power_detection_cpp",
                     gr::io_signature::make(num_inputs, num_inputs, sizeof(gr_complex)),
                     gr::io_signature::make(num_inputs, num_inputs, sizeof(gr_complex))),
      d_num_inputs(num_inputs),
      d_sample_rate(sample_rate),
      d_threshold(threshold),
      d_buffer_size(buffer_size),
      d_capture_index(0),
      d_playback_index(0),
      d_capturing(false),
      d_playback_buffer_valid(false),
      d_buffer_fill_complete(false),
      d_averaging_window(10),
      d_power_buffer_index(0),
      d_power_sum(0.0f)
{
    // Allocate buffers for all channels
    d_capture_buffer.resize(num_inputs);
    d_playback_buffer.resize(num_inputs);
    
    for (int ch = 0; ch < num_inputs; ch++) {
        d_capture_buffer[ch].resize(buffer_size);
        d_playback_buffer[ch].resize(buffer_size);
    }
    
    // Initialize power averaging buffer
    d_power_buffer.resize(d_averaging_window, 0.0f);
    
    GR_LOG_INFO(d_logger, "Power detection initialized: " + 
                std::to_string(num_inputs) + " channels, threshold=" + 
                std::to_string(threshold) + ", buffer=" + std::to_string(buffer_size) +
                ", averaging_window=" + std::to_string(d_averaging_window));
}

power_detection_cpp_impl::~power_detection_cpp_impl() {}

void power_detection_cpp_impl::validate_and_promote_buffer()
{
    // Copy capture buffer to playback buffer for all channels
    for (int ch = 0; ch < d_num_inputs; ch++) {
        std::memcpy(d_playback_buffer[ch].data(),
                   d_capture_buffer[ch].data(),
                   d_buffer_size * sizeof(gr_complex));
    }
    
    d_playback_buffer_valid = true;
    d_buffer_fill_complete = true;
    d_playback_index = 0;
    
    GR_LOG_INFO(d_logger, "Buffer filled completely! Promoted to playback buffer");
}

int power_detection_cpp_impl::work(int noutput_items,
                                  gr_vector_const_void_star& input_items,
                                  gr_vector_void_star& output_items)
{
    // Get pointer to first channel for power detection
    const gr_complex* in0 = static_cast<const gr_complex*>(input_items[0]);
    
    // Process each sample
    for (int i = 0; i < noutput_items; i++) {
        // Calculate instantaneous power on first channel
        gr_complex sample = in0[i];
        float sample_power = std::norm(sample);  // |sample|^2 (faster than abs()^2)
        
        // Update circular buffer for averaging
        d_power_sum -= d_power_buffer[d_power_buffer_index];
        d_power_buffer[d_power_buffer_index] = sample_power;
        d_power_sum += sample_power;
        d_power_buffer_index = (d_power_buffer_index + 1) % d_averaging_window;
        
        // Calculate averaged power
        float avg_power = d_power_sum / d_averaging_window;
        
        // Threshold-based detection using averaged power
        if (avg_power > d_threshold) {
            // Start capturing if not already
            if (!d_capturing) {
                d_capturing = true;
                d_capture_index = 0;
                GR_LOG_INFO(d_logger, "Signal detected! Power: " + std::to_string(avg_power));
            }
            
            // Fill capture buffer for all channels
            if (d_capture_index < d_buffer_size) {
                for (int ch = 0; ch < d_num_inputs; ch++) {
                    const gr_complex* in_ch = static_cast<const gr_complex*>(input_items[ch]);
                    d_capture_buffer[ch][d_capture_index] = in_ch[i];
                }
                d_capture_index++;
                
                // Check if buffer is now full
                if (d_capture_index >= d_buffer_size) {
                    validate_and_promote_buffer();
                }
            }
            
            // Pass through all channels during detection
            for (int ch = 0; ch < d_num_inputs; ch++) {
                const gr_complex* in_ch = static_cast<const gr_complex*>(input_items[ch]);
                gr_complex* out_ch = static_cast<gr_complex*>(output_items[ch]);
                out_ch[i] = in_ch[i];
            }
            
        } else {
            // No signal - stop capturing and replay if available
            if (d_capturing) {
                d_capturing = false;
                if (d_capture_index > 0 && !d_buffer_fill_complete) {
                    GR_LOG_INFO(d_logger, "Signal ended with " + 
                               std::to_string(d_capture_index) + " samples (buffer not full)");
                }
            }
            
            // Replay stored signal during silence for all channels
            if (d_playback_buffer_valid && d_buffer_fill_complete) {
                for (int ch = 0; ch < d_num_inputs; ch++) {
                    gr_complex* out_ch = static_cast<gr_complex*>(output_items[ch]);
                    out_ch[i] = d_playback_buffer[ch][d_playback_index];
                }
                d_playback_index = (d_playback_index + 1) % d_buffer_size;
            } else {
                // No valid signal captured yet - output zeros on all channels
                for (int ch = 0; ch < d_num_inputs; ch++) {
                    gr_complex* out_ch = static_cast<gr_complex*>(output_items[ch]);
                    out_ch[i] = gr_complex(0, 0);
                }
            }
        }
    }
    
    return noutput_items;
}

} /* namespace doa */
} /* namespace gr */
