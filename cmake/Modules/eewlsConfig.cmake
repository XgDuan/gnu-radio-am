INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_EEWLS eewls)

FIND_PATH(
    EEWLS_INCLUDE_DIRS
    NAMES eewls/api.h
    HINTS $ENV{EEWLS_DIR}/include
        ${PC_EEWLS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    EEWLS_LIBRARIES
    NAMES gnuradio-eewls
    HINTS $ENV{EEWLS_DIR}/lib
        ${PC_EEWLS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(EEWLS DEFAULT_MSG EEWLS_LIBRARIES EEWLS_INCLUDE_DIRS)
MARK_AS_ADVANCED(EEWLS_LIBRARIES EEWLS_INCLUDE_DIRS)

