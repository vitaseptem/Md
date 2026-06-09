cmake_minimum_required(VERSION 3.16)

project(valen_vault_engine
    VERSION 1.0.0
    DESCRIPTION "VALEN Vault Engine v1 - motor de memoria persistente do VALEN"
    LANGUAGES CXX)

# --- Padrao C++20 (obrigatorio) ---------------------------------------
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Build Release por padrao se nada for especificado.
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# Binario na raiz do build para facilitar o uso.
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# --- nlohmann/json (header-only) --------------------------------------
# Estrategia v1: header vendorizado em core/include/nlohmann/json.hpp.
# Caso o header nao exista localmente, faz fallback para FetchContent.
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/include/nlohmann/json.hpp")
    message(STATUS "Usando nlohmann/json vendorizado em include/nlohmann/json.hpp")
    set(VALEN_JSON_VENDORED ON)
else()
    message(STATUS "nlohmann/json nao encontrado localmente; usando FetchContent")
    include(FetchContent)
    FetchContent_Declare(
        nlohmann_json
        GIT_REPOSITORY https://github.com/nlohmann/json.git
        GIT_TAG v3.11.3
    )
    FetchContent_MakeAvailable(nlohmann_json)
endif()

# --- Executavel -------------------------------------------------------
add_executable(valen
    src/main.cpp
    src/vault_engine.cpp
    src/note.cpp
    src/link_resolver.cpp
    src/indexer.cpp
)

target_include_directories(valen PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

if(NOT VALEN_JSON_VENDORED)
    target_link_libraries(valen PRIVATE nlohmann_json::nlohmann_json)
endif()

# Avisos uteis (sem -Werror para nao travar build em compiladores variados).
if(MSVC)
    target_compile_options(valen PRIVATE /W4)
else()
    target_compile_options(valen PRIVATE -Wall -Wextra)
endif()
