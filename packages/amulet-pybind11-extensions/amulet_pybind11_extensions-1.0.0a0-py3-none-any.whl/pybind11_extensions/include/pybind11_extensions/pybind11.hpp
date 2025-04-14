#pragma once
#include <pybind11/pybind11.h>

#include "builtins.hpp"
#include "collections.hpp"

namespace pybind11_extensions {

// Create a python iterator around a C++ class that implements method next()
// Next should throw py::stop_iteration() to signal the end of the iterator.
template <
    typename T,
    pybind11::return_value_policy Policy = pybind11::return_value_policy::automatic,
    typename... Extra>
auto make_iterator(T&& obj, Extra&&... extra) -> pybind11_extensions::collections::abc::Iterator<decltype(obj.next())>
{
    if (!pybind11::detail::get_type_info(typeid(T), false)) {
        pybind11::class_<T>(pybind11::handle(), "iterator", pybind11::module_local())
            .def(
                "__iter__",
                [](
                    pybind11_extensions::PyObjectCpp<T>& s) -> pybind11_extensions::PyObjectCpp<T>& { return s; })
            .def(
                "__next__",
                [](T& s) -> decltype(obj.next()) {
                    return s.next();
                },
                std::forward<Extra>(extra)...,
                Policy);
    }
    return pybind11::cast(std::move(obj));
}

} // namespace pybind11_extensions
