cmake_minimum_required(VERSION 3.10)
project(Simd)

option(SIMD_AVX512 "AVX-512 (AVX-512F, AVX-512CD, AVX-512VL, AVX-512DQ, AVX-512BW) enable" ON)
option(SIMD_AVX512VNNI "AVX-512-VNNI enable" ON)
option(SIMD_TEST "Test framework enable" ON)
option(SIMD_INFO "Print build information" ON) #TODO delete it
option(SIMD_PERF "Internal performance statistic" OFF)
option(SIMD_SHARED "Build as SHARED library" ON)
option(SIMD_GET_VERSION "Get Simd Library version" ON)
option(SIMD_SYNET "Synet optimizations enable" ON)
option(SIMD_INT8_DEBUG "Synet INT8 debug enable" OFF)
option(SIMD_HIDE "Hide internal functions of Simd Library" OFF)
#set(MAX_ERRORS 5)

if ((NOT DEFINED SIMD_ROOT) OR (SIMD_ROOT STREQUAL ""))
    set(SIMD_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../..")
endif ()

#if((NOT DEFINED CMAKE_BUILD_TYPE) OR (CMAKE_BUILD_TYPE STREQUAL ""))
#    set(CMAKE_BUILD_TYPE "Release")
#endif()

#if(NOT ${SIMD_TARGET} STREQUAL "")
#    set(CMAKE_SYSTEM_PROCESSOR ${SIMD_TARGET})
#endif()

if (SIMD_HIDE AND SIMD_TEST)
    message(FATAL_ERROR "Test framework requires access to internal functions!")
endif ()

#if (NOT SIMD_TOOLCHAIN STREQUAL "")
#    set(CMAKE_C_COMPILER ${SIMD_TOOLCHAIN})
#    set(CMAKE_CXX_COMPILER ${SIMD_TOOLCHAIN})
#    execute_process(COMMAND "${CMAKE_CXX_COMPILER}" -dumpversion OUTPUT_VARIABLE CMAKE_CXX_COMPILER_VERSION)
#    string(REGEX REPLACE "\n$" "" CMAKE_CXX_COMPILER_VERSION "${CMAKE_CXX_COMPILER_VERSION}")
#endif ()

if (SIMD_INFO)
    message(DEBUG "Simd Library:")
    message(DEBUG "Build type: '${CMAKE_BUILD_TYPE}'")
    message(DEBUG "Target: ${CMAKE_SYSTEM_PROCESSOR}")
    message(DEBUG "Library type: ${SIMD_LIB_TYPE}")
    message(DEBUG "Toolchain: ${CMAKE_CXX_COMPILER}")
    message(DEBUG "Compiler ID: ${CMAKE_CXX_COMPILER_ID}")
    message(DEBUG "Compiler Version: ${CMAKE_CXX_COMPILER_VERSION}")
    message(DEBUG "Test framework: ${SIMD_TEST}")
    message(DEBUG "Performance statistic: ${SIMD_PERF}")
    message(DEBUG "Synet: ${SIMD_SYNET}")
    message(DEBUG "Debug INT8: ${SIMD_INT8_DEBUG}")
    message(DEBUG "Hide internal: ${SIMD_HIDE}")
    if (NOT ${SIMD_TEST_FLAGS} STREQUAL "")
        message(DEBUG "Test flags: ${SIMD_TEST_FLAGS}")
    endif ()
endif ()

set(SIMD_LIB_NAME Simd)
if (SIMD_SHARED)
    add_library(${SIMD_LIB_NAME} SHARED)
else ()
    add_library(${SIMD_LIB_NAME} STATIC)
endif ()

if (NOT SIMD_SYNET)
    target_compile_definitions(${SIMD_LIB_NAME} PRIVATE SIMD_SYNET_DISABLE)
endif ()

if (NOT SIMD_INT8_DEBUG)
    target_compile_definitions(${SIMD_LIB_NAME} PRIVATE SIMD_INT8_DEBUG_DISABLE)
endif ()

if (SIMD_HIDE)
    target_compile_definitions(${SIMD_LIB_NAME} PRIVATE SIMD_HIDE_INTERNAL)
endif ()

if (SIMD_PERF)
    target_compile_definitions(${SIMD_LIB_NAME} PRIVATE DSIMD_PERFORMANCE_STATISTIC)
endif ()

target_include_directories(${SIMD_LIB_NAME} PUBLIC
        $<BUILD_INTERFACE:${SIMD_ROOT}/src>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

if (SIMD_GET_VERSION)
    if (WIN32)
        execute_process(COMMAND "${SIMD_ROOT}/prj/cmd/GetVersion.cmd" "${SIMD_ROOT}")
    else ()
        execute_process(COMMAND bash "${SIMD_ROOT}/prj/sh/GetVersion.sh" "${SIMD_ROOT}")
    endif ()
else ()
    target_compile_definitions(${SIMD_LIB_NAME} PRIVATE SIMD_VERSION=unknown)
endif ()

set_property(TARGET ${SIMD_LIB_NAME} PROPERTY POSITION_INDEPENDENT_CODE ON)

#TODO ???
#string(REGEX REPLACE "(-march=[a-zA-Z0-9-]*)|(-mtune=[a-zA-Z0-9-]*)|(-msse[0-9,\\.]*)|(-mavx[0-9]*)|(-mfma)" "" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")

#if (CMAKE_BUILD_TYPE STREQUAL "Release")
#    set(COMMON_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -std=c++11 -O3")
#elseif (CMAKE_BUILD_TYPE STREQUAL "Debug")
#    set(COMMON_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -std=c++11 -O0 -g")
#else ()
#    message(FATAL_ERROR "Unknown value of CMAKE_BUILD_TYPE!")
#endif ()

#if ((CMAKE_CXX_COMPILER MATCHES "clang") OR (CMAKE_CXX_COMPILER_ID MATCHES "Clang"))
#    set(COMMON_CXX_FLAGS "${COMMON_CXX_FLAGS} -ferror-limit=${MAX_ERRORS}")
#else ()
#    set(COMMON_CXX_FLAGS "${COMMON_CXX_FLAGS} -fmax-errors=${MAX_ERRORS}")
#endif ()

#if (SIMD_HIDE)
#    set(COMMON_CXX_FLAGS "${COMMON_CXX_FLAGS} -fvisibility=hidden")
#endif ()

include(simd_base_files.cmake)
target_sources(${SIMD_LIB_NAME} PRIVATE ${SIMD_BASE_SOURCES})

if (CMAKE_SYSTEM_PROCESSOR MATCHES "(x86_64)|(AMD64|amd64)|(^i.86$)")
    include(x86.cmake)
elseif (CMAKE_SYSTEM_PROCESSOR MATCHES "^(aarch64|arm|arm64)")
    include(arm.cmake)
elseif (CMAKE_SYSTEM_PROCESSOR MATCHES "^(ppc|ppc64)")
    include(ppc.cmake)
else ()
    message(FATAL_ERROR "Unknown value of CMAKE_SYSTEM_PROCESSOR!")
endif ()

file(STRINGS ../txt/FullVersion.txt SIMD_LIB_VERSION)

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

configure_package_config_file(${CMAKE_CURRENT_SOURCE_DIR}/SimdConfig.cmake.in
        "${CMAKE_CURRENT_BINARY_DIR}/SimdConfig.cmake"
        INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/Simd
        )

write_basic_package_version_file(
        ${CMAKE_CURRENT_BINARY_DIR}/SimdConfigVersion.cmake
        VERSION ${SIMD_LIB_VERSION}
        COMPATIBILITY SameMajorVersion)

install(TARGETS ${SIMD_LIB_NAME} EXPORT Simd ARCHIVE LIBRARY)
install(EXPORT Simd DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/Simd NAMESPACE Simd::)
install(DIRECTORY ${SIMD_ROOT}/src/Simd DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        FILES_MATCHING PATTERN "*.h")
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/SimdConfig.cmake
        ${CMAKE_CURRENT_BINARY_DIR}/SimdConfigVersion.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/Simd)
