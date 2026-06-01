cmake_minimum_required(VERSION 3.10)

project(UAV_GCS_CPP)

set(CMAKE_CXX_STANDARD 17)

add_library(
    telemetry_core
    src/telemetry_core.cpp
)
