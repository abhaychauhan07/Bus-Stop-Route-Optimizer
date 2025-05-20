from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "graph_module",
        ["graph.cpp", "graph_binding.cpp"],
        include_dirs=[pybind11.get_include()],
        language='c++'
    ),
]

setup(
    name="graph_module",
    ext_modules=ext_modules,
    python_requires=">=3.6",
) 