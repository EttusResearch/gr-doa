INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_DOA doa)

FIND_PATH(
    DOA_INCLUDE_DIRS
    NAMES doa/api.h
    HINTS $ENV{DOA_DIR}/include
        ${PC_DOA_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    DOA_LIBRARIES
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

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(DOA DEFAULT_MSG DOA_LIBRARIES DOA_INCLUDE_DIRS)
MARK_AS_ADVANCED(DOA_LIBRARIES DOA_INCLUDE_DIRS)

