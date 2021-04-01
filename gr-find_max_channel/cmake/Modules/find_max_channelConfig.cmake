INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_FIND_MAX_CHANNEL find_max_channel)

FIND_PATH(
    FIND_MAX_CHANNEL_INCLUDE_DIRS
    NAMES find_max_channel/api.h
    HINTS $ENV{FIND_MAX_CHANNEL_DIR}/include
        ${PC_FIND_MAX_CHANNEL_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    FIND_MAX_CHANNEL_LIBRARIES
    NAMES gnuradio-find_max_channel
    HINTS $ENV{FIND_MAX_CHANNEL_DIR}/lib
        ${PC_FIND_MAX_CHANNEL_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/find_max_channelTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(FIND_MAX_CHANNEL DEFAULT_MSG FIND_MAX_CHANNEL_LIBRARIES FIND_MAX_CHANNEL_INCLUDE_DIRS)
MARK_AS_ADVANCED(FIND_MAX_CHANNEL_LIBRARIES FIND_MAX_CHANNEL_INCLUDE_DIRS)
