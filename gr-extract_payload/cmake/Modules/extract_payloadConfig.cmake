INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_EXTRACT_PAYLOAD extract_payload)

FIND_PATH(
    EXTRACT_PAYLOAD_INCLUDE_DIRS
    NAMES extract_payload/api.h
    HINTS $ENV{EXTRACT_PAYLOAD_DIR}/include
        ${PC_EXTRACT_PAYLOAD_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    EXTRACT_PAYLOAD_LIBRARIES
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

include("${CMAKE_CURRENT_LIST_DIR}/extract_payloadTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(EXTRACT_PAYLOAD DEFAULT_MSG EXTRACT_PAYLOAD_LIBRARIES EXTRACT_PAYLOAD_INCLUDE_DIRS)
MARK_AS_ADVANCED(EXTRACT_PAYLOAD_LIBRARIES EXTRACT_PAYLOAD_INCLUDE_DIRS)
