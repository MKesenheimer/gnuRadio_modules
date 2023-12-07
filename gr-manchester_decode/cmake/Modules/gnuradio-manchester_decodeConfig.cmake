find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_MANCHESTER_DECODE gnuradio-manchester_decode)

FIND_PATH(
    GR_MANCHESTER_DECODE_INCLUDE_DIRS
    NAMES gnuradio/manchester_decode/api.h
    HINTS $ENV{MANCHESTER_DECODE_DIR}/include
        ${PC_MANCHESTER_DECODE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_MANCHESTER_DECODE_LIBRARIES
    NAMES gnuradio-manchester_decode
    HINTS $ENV{MANCHESTER_DECODE_DIR}/lib
        ${PC_MANCHESTER_DECODE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-manchester_decodeTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_MANCHESTER_DECODE DEFAULT_MSG GR_MANCHESTER_DECODE_LIBRARIES GR_MANCHESTER_DECODE_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_MANCHESTER_DECODE_LIBRARIES GR_MANCHESTER_DECODE_INCLUDE_DIRS)
