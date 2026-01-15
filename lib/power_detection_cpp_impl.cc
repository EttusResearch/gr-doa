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
power_detection_cpp::make(int num_inputs, double sample_rate, int buffer_size, float threshold_multiplier)
{
    return gnuradio::make_block_sptr<power_detection_cpp_impl>(
        num_inputs, sample_rate, buffer_size, threshold_multiplier);
}

power_detection_cpp_impl::power_detection_cpp_impl(int num_inputs,
                                                   double sample_rate,
                                                   int buffer_size,
                                                   float threshold_multiplier)
    : gr::sync_block("power_detection_cpp",
                     gr::io_signature::make(num_inputs, num_inputs, sizeof(gr_complex)),
                     gr::io_signature::make(num_inputs, num_inputs, sizeof(gr_complex))),
      d_num_inputs(num_inputs),
      d_sample_rate(sample_rate),
      d_buffer_size(buffer_size),
      d_capture_index(0),
      d_playback_index(0),
      d_playback_size(0),
      d_capturing(false),
      d_playback_buffer_valid(false),
      d_buffer_fill_complete(false),
      d_averaging_window(40),
      d_power_buffer_index(0),
      d_power_sum(0.0f),
      d_lowest_power_sum(1.0f),
      d_threshold_multiplier(threshold_multiplier)
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
                std::to_string(num_inputs) + " channels, buffer=" + std::to_string(buffer_size) +
                ", averaging_window=" + std::to_string(d_averaging_window) +
                ", threshold_multiplier=" + std::to_string(d_threshold_multiplier));
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
    d_playback_size = d_buffer_size;
    
    GR_LOG_INFO(d_logger, "Buffer filled completely! Promoted to playback buffer (" + 
                std::to_string(d_playback_size) + " samples)");
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
        
        // Dynamic threshold: track minimum power seen, set threshold to threshold_multiplier that for noise rejection
        if (d_power_sum < d_lowest_power_sum) {
            d_lowest_power_sum = d_power_sum;
        }
        
        d_threshold = d_lowest_power_sum * d_threshold_multiplier;
        
        // Slowly increase lowest power sum to adapt to changing noise floor
        d_lowest_power_sum *= 1.000001f;
        // Ensure minimum threshold to avoid triggering on very low noise
        d_threshold = std::max(d_threshold, 0.0000001f);

        // Calculate averaged power
        float avg_power = d_power_sum / d_averaging_window;
        
        // Log debug info every 1000th sample
        /*
        static int debug_counter = 0;
        debug_counter++;
        if (debug_counter % 1000 == 0) {
            GR_LOG_INFO(d_logger, "Avg power: " + std::to_string(avg_power) + ", Threshold: " + std::to_string(d_threshold) + ", Capturing: " + std::to_string(d_capturing));
        }
        */

        // Threshold-based detection using averaged power
        if (avg_power > d_threshold) {
            // Start capturing if not already
            if (!d_capturing) {
                d_capturing = true;
                d_capture_index = 0;
                GR_LOG_INFO(d_logger, "Signal detected! Power: " + std::to_string(avg_power));
            }
            
            // Always fill capture buffer for all channels (in background)
            for (int ch = 0; ch < d_num_inputs; ch++) {
                const gr_complex* in_ch = static_cast<const gr_complex*>(input_items[ch]);
                
                d_capture_buffer[ch][d_capture_index] = in_ch[i];
            }
            d_capture_index++;
            
            // Check if buffer is now full
            if (d_capture_index >= d_buffer_size) {
                validate_and_promote_buffer();
                d_capture_index = 0;  // Reset for next capture
            }
        } else {
            // No signal - stop capturing and promote buffer if we have data
            if (d_capturing) {
                d_capturing = false;
                if (d_capture_index > 0) {
                    GR_LOG_INFO(d_logger, "Signal ended with " + 
                               std::to_string(d_capture_index) + " samples (partial buffer)");
                    // Don't promote partial buffers - wait for full buffer from validate_and_promote_buffer()
                }
            }
        }
        
        // Output: Always use playback buffer if valid, otherwise pass through
        static int playback_samples = 0;
        static int passthrough_samples = 0;
        static int last_report = 0;
        
        if (d_playback_buffer_valid && d_buffer_fill_complete) {
            // Continuous replay of stored signal
            for (int ch = 0; ch < d_num_inputs; ch++) {
                gr_complex* out_ch = static_cast<gr_complex*>(output_items[ch]);
                out_ch[i] = d_playback_buffer[ch][d_playback_index];
            }
            d_playback_index = (d_playback_index + 1) % d_playback_size;
            playback_samples++;
        } else {
            // No valid buffer yet - pass through real signal
            for (int ch = 0; ch < d_num_inputs; ch++) {
                const gr_complex* in_ch = static_cast<const gr_complex*>(input_items[ch]);
                gr_complex* out_ch = static_cast<gr_complex*>(output_items[ch]);
                out_ch[i] = in_ch[i];
            }
            passthrough_samples++;
        }
        
        // Report statistics every 2.5M samples (1 second @ 2.5 MHz)
        if ((playback_samples + passthrough_samples - last_report) >= 2500000) {
            GR_LOG_INFO(d_logger, "Output stats - Playback: " + std::to_string(playback_samples) +
                       " samples (" + std::to_string(100.0 * playback_samples / (playback_samples + passthrough_samples)) +
                       "%), Passthrough: " + std::to_string(passthrough_samples) + " samples");
            last_report = playback_samples + passthrough_samples;
        }
    }
    
    return noutput_items;
}

} /* namespace doa */
} /* namespace gr */
