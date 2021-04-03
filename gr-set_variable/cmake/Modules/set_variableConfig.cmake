INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SET_VARIABLE set_variable)

FIND_PATH(
    SET_VARIABLE_INCLUDE_DIRS
    NAMES set_variable/api.h
    HINTS $ENV{SET_VARIABLE_DIR}/include
        ${PC_SET_VARIABLE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SET_VARIABLE_LIBRARIES
    NAMES gnuradio-set_variable
    HINTS $ENV{SET_VARIABLE_DIR}/lib
        ${PC_SET_VARIABLE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/set_variableTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SET_VARIABLE DEFAULT_MSG SET_VARIABLE_LIBRARIES SET_VARIABLE_INCLUDE_DIRS)
MARK_AS_ADVANCED(SET_VARIABLE_LIBRARIES SET_VARIABLE_INCLUDE_DIRS)
