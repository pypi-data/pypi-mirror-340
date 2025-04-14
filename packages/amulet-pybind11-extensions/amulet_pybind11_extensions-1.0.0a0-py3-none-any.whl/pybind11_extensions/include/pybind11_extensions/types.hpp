#pragma once
#include <pybind11/pybind11.h>
#include "builtins.hpp"

// This extension adds a py::object subclass for types.NotImplementedType.
// This is used as a return in comparison operators.


namespace pybind11_extensions {
    namespace types {
        using NotImplementedType = pybind11_extensions::PyObjectStr<"types.NotImplementedType">;
    }
}
