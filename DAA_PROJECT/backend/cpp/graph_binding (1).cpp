#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "graph.hpp"

namespace py = pybind11;

PYBIND11_MODULE(graph_module, m) {
    py::class_<BusStop>(m, "BusStop")
        .def(py::init<>())
        .def_readwrite("id", &BusStop::id)
        .def_readwrite("name", &BusStop::name)
        .def_readwrite("latitude", &BusStop::latitude)
        .def_readwrite("longitude", &BusStop::longitude);

    py::class_<Graph>(m, "Graph")
        .def(py::init<int>())
        .def("addEdge", &Graph::addEdge)
        .def("addBusStop", &Graph::addBusStop)
        .def("shortestPath", &Graph::shortestPath)
        .def("getPathDistance", &Graph::getPathDistance)
        .def("getBusStop", &Graph::getBusStop);
} 