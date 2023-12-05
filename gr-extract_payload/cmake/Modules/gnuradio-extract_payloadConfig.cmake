find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_EXTRACT_PAYLOAD gnuradio-extract_payload)

FIND_PATH(
    GR_EXTRACT_PAYLOAD_INCLUDE_DIRS
    NAMES gnuradio/extract_payload/api.h
    HINTS $ENV{EXTRACT_PAYLOAD_DIR}/include
        ${PC_EXTRACT_PAYLOAD_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_EXTRACT_PAYLOAD_LIBRARIES
    NAMES gnuradio-extract_payload
    HINTS $ENV{EXTRACT_PAYLOAD_DIR}/lib
        ${PC_EXTRACT_PAYLOAD_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-extract_payloadTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_EXTRACT_PAYLOAD DEFAULT_MSG GR_EXTRACT_PAYLOAD_LIBRARIES GR_EXTRACT_PAYLOAD_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_EXTRACT_PAYLOAD_LIBRARIES GR_EXTRACT_PAYLOAD_INCLUDE_DIRS)
