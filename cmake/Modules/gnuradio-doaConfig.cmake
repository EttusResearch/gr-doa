find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_DOA gnuradio-doa)

FIND_PATH(
    GR_DOA_INCLUDE_DIRS
    NAMES gnuradio/doa/api.h
    HINTS $ENV{DOA_DIR}/include
        ${PC_DOA_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_DOA_LIBRARIES
    NAMES gnuradio-doa
    HINTS $ENV{DOA_DIR}/lib
        ${PC_DOA_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-doaTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_DOA DEFAULT_MSG GR_DOA_LIBRARIES GR_DOA_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_DOA_LIBRARIES GR_DOA_INCLUDE_DIRS)
