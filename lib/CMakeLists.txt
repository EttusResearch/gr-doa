# Copyright 2011,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})
list(APPEND doa_sources
    autocorrelate_impl.cc
    MUSIC_lin_array_impl.cc
    rootMUSIC_linear_array_impl.cc
    antenna_correction_impl.cc
    find_local_max_impl.cc
    calibrate_lin_array_impl.cc
    )

set(doa_sources "${doa_sources}" PARENT_SCOPE)
if(NOT doa_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT doa_sources)

add_library(gnuradio-doa SHARED ${doa_sources})
target_link_libraries(gnuradio-doa ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES} ${ARMADILLO_LIBRARIES})
set_target_properties(gnuradio-doa PROPERTIES DEFINE_SYMBOL "gnuradio_doa_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-doa PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
install(TARGETS gnuradio-doa
    LIBRARY DESTINATION lib${LIB_SUFFIX} # .so/.dylib file
    ARCHIVE DESTINATION lib${LIB_SUFFIX} # .lib file
    RUNTIME DESTINATION bin              # .dll file
)
