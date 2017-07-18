set(CMAKE_INSTALL_PREFIX ${PROJECT_BINARY_DIR})

unset(CMAKE_LIBRARY_ARCHITECTURE)

include(GNUInstallDirs)
include(ConfigProjectVersion)
include(ConfigSafeGuards)
include(ConfigGitRevision)

find_package(Python REQUIRED)
set(PYTHON_SITE_INSTALL_DIR
    lib/python${PYTHON_VERSION}/site-packages/gimic)
include(UseCython)
include(ConfigTesting)
include(ConfigPackaging)

set(CMAKE_Fortran_MODULE_DIRECTORY ${CMAKE_BINARY_DIR}/modules)

configure_file (
    ${PROJECT_SOURCE_DIR}/config.h.in
    ${PROJECT_BINARY_DIR}/config.h
    )

add_subdirectory(tools)
add_subdirectory(test)
