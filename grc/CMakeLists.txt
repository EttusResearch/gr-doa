# Copyright 2011 Free Software Foundation, Inc.
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
install(FILES
    phase_correct_hier.xml
    twinrx_usrp_source.xml
    doa_autocorrelate.xml
    doa_MUSIC_lin_array.xml
    doa_average_and_save.xml
    doa_rootMUSIC_linear_array.xml
    doa_qt_compass.xml
    doa_antenna_correction.xml
    doa_save_antenna_calib.xml
    doa_twinrx_phase_offset_est.xml
    doa_findmax_and_save.xml
    doa_find_local_max.xml
    doa_calibrate_lin_array.xml
    DESTINATION share/gnuradio/grc/blocks
)
