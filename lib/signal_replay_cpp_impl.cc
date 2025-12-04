/* -*- c++ -*- */
/*
 * Copyright 2025 Ettus Research LLC.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "signal_replay_cpp_impl.h"
#include <gnuradio/io_signature.h>
#include <fstream>
#include <cstring>
#include <stdexcept>

namespace gr {
namespace doa {

signal_replay_cpp::sptr
signal_replay_cpp::make(const std::string& filename, bool repeat, int interpolation)
{
    return gnuradio::make_block_sptr<signal_replay_cpp_impl>(filename, repeat, interpolation);
}

signal_replay_cpp_impl::signal_replay_cpp_impl(const std::string& filename,
                                             bool repeat,
                                             int interpolation)
    : gr::sync_block("signal_replay_cpp",
                     gr::io_signature::make(0, 0, 0),
                     gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_position(0),
      d_repeat(repeat),
      d_interpolation(interpolation),
      d_filename(filename)
{
    if (!load_numpy_file(filename)) {
        GR_LOG_ERROR(d_logger, "Failed to load signal file, using zero signal");
        d_signal_data.resize(1);
        d_signal_data[0] = gr_complex(0, 0);
    }
}

signal_replay_cpp_impl::~signal_replay_cpp_impl() {}

bool signal_replay_cpp_impl::load_numpy_file(const std::string& filename)
{
    // Simple .npy loader for complex64 data
    // Full .npy format: https://numpy.org/devdocs/reference/generated/numpy.lib.format.html
    
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        GR_LOG_ERROR(d_logger, "Cannot open file: " + filename);
        return false;
    }

    // Read .npy magic number and version / check if it is a valid .npy file
    char magic[6];
    file.read(magic, 6);
    if (std::strncmp(magic, "\x93NUMPY", 6) != 0) {
        GR_LOG_ERROR(d_logger, "Not a valid .npy file");
        return false;
    }

    uint8_t major_version, minor_version;
    file.read(reinterpret_cast<char*>(&major_version), 1);
    file.read(reinterpret_cast<char*>(&minor_version), 1);

    // Read header length
    uint16_t header_len;
    if (major_version == 1) {
        file.read(reinterpret_cast<char*>(&header_len), 2);
    } else {
        uint32_t header_len_32;
        file.read(reinterpret_cast<char*>(&header_len_32), 4);
        header_len = static_cast<uint16_t>(header_len_32);
    }

    // Skip header (contains dtype)
    file.seekg(header_len, std::ios::cur);

    // Read all remaining data as complex floats
    file.seekg(0, std::ios::end);
    size_t file_size = file.tellg();

    file.seekg(10 + header_len, std::ios::beg); // Skip to data

    size_t data_size = file_size - (10 + header_len);
    size_t num_samples = data_size / sizeof(gr_complex);

    d_signal_data.resize(num_samples);
    file.read(reinterpret_cast<char*>(d_signal_data.data()), data_size);

    GR_LOG_INFO(d_logger, "Loaded " + std::to_string(num_samples) + " samples from " + filename);
    return true;
}

int signal_replay_cpp_impl::work(int noutput_items,
                                gr_vector_const_void_star& input_items,
                                gr_vector_void_star& output_items)
{
    gr_complex* out = static_cast<gr_complex*>(output_items[0]);
    // Handle empty signal case
    if (d_signal_data.empty()) {
        std::memset(out, 0, noutput_items * sizeof(gr_complex));
        return noutput_items;
    }

    // Fast path: no interpolation (interpolation factor = 1)
    // This optimized path uses chunked memcpy operations instead of copying sample-by-sample
    if (d_interpolation == 1) {
        int samples_written = 0;
        size_t signal_len = d_signal_data.size();
        
        // Keep filling the output buffer until we've written all requested samples
        while (samples_written < noutput_items) {
            // Check if we've reached the end of the signal data
            if (d_position >= signal_len) {
                if (d_repeat) {
                    // Wrap around to the beginning of the signal for continuous playback
                    d_position = 0;
                } else {
                    // Fill remaining output buffer with zeros and stop
                    std::memset(out + samples_written, 0, 
                               (noutput_items - samples_written) * sizeof(gr_complex));
                    return samples_written;
                }
            }

            // Calculate the maximum number of samples we can copy in this iteration
            // Limited by either: remaining output space OR remaining signal data
            size_t samples_to_copy = std::min(
                static_cast<size_t>(noutput_items - samples_written),  // Space left in output
                signal_len - d_position                                // Samples left before signal end
            );

            // Copy the chunk of samples efficiently using memcpy
            std::memcpy(out + samples_written,                  // Destination in output buffer
                       d_signal_data.data() + d_position,       // Source in signal data
                       samples_to_copy * sizeof(gr_complex));   // Number of bytes to copy

            // Advance our position in the signal data
            d_position += samples_to_copy;
            // Track how many samples we've written to the output
            samples_written += samples_to_copy;
        }
        return noutput_items;
    }

    // Slow path: with interpolation - not used often
    int samples_written = 0;
    size_t signal_len = d_signal_data.size();

    while (samples_written < noutput_items) {
        size_t source_idx = d_position / d_interpolation;

        if (source_idx >= signal_len) {
            if (d_repeat) {
                d_position = 0;
                continue;
            } else {
                std::memset(out + samples_written, 0, 
                           (noutput_items - samples_written) * sizeof(gr_complex));
                return samples_written;
            }
        }

        out[samples_written++] = d_signal_data[source_idx];
        d_position++;
    }
    return noutput_items;
}

} /* namespace doa */
} /* namespace gr */
