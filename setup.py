import os
from setuptools import setup

def read(fname):
	return open(fname, "r").read()

setup(
	name = "PythonToolsForGeomechanics",
	version = "0.0.1",
	author = "Herminio Tasinafo Honorio",
	author_email = "herminio.eng@gmail.com",
	description = ("This package is intended to support and manage results generated from geomechanical problems."),
	license = "BSD",
	packages = ["AnalyticalSolutions", "Examples", "CGNSTools", "PhysicalPropertyTools"],
	package_data = {"CGNSTools" : ["Results/Results.cgns"],
					"PhysicalPropertyTools" : ["Json_Files/solid.json", "Json_Files/fluid.json"]},
	long_description = read("README.txt"),
)