if (NOT TARGET pybind11_extensions)
    set(pybind11_extensions_INCLUDE_DIR "${CMAKE_CURRENT_LIST_DIR}/include")

    add_library(pybind11_extensions IMPORTED INTERFACE)
    set_target_properties(pybind11_extensions PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES "${pybind11_extensions_INCLUDE_DIR}"
    )
endif()
