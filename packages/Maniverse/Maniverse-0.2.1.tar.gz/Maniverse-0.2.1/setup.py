import os
import wget
import tarfile
import subprocess
from setuptools import setup, find_packages
from setuptools.command.build import build

class CustomBuild(build):
	def run(self):

		pwd = os.path.dirname(__file__)

		# Checking commands
		MAKE = os.getenv("MAKE", default = "make")
		print("MAKE is %s." % MAKE)
		CXX = os.getenv("CXX", default = "g++")
		print("CXX is %s." % CXX)
		AR = os.getenv("AR", default = "ar")
		print("AR is %s." % AR)

		# Checking dependencies
		PYTHON3 = os.getenv("PYTHON3", default = '')
		print("Looking for Python.h at %s ..." % PYTHON3, end='')
		if os.path.isfile(PYTHON3 + "/Python.h"):
			print("Found!")
		else:
			raise RuntimeError("Python.h does not exist!")
		EIGEN3 = os.getenv("EIGEN3", default = '')
		if len(EIGEN3) > 0:
			print("Looking for Eigen3 at %s ..." % EIGEN3, end='')
			if os.path.exists(EIGEN3 + "/Eigen/") and os.path.exists(EIGEN3 + "/unsupported/") and os.path.isfile(EIGEN3 + "/signature_of_eigen3_matrix_library"):
				print("Found!")
			else:
				raise RuntimeError("Python.h does not exist!")
		else:
			print("The environment variable $EIGEN3 is not set. -> Downloading ...")
			filename = wget.download("https://gitlab.com/libeigen/eigen/-/archive/3.4-rc1/eigen-3.4-rc1.tar.gz", bar = None)
			with tarfile.open(filename) as tar:
				tar.extractall(path = pwd) # Directory: eigen-3.4-rc1
			EIGEN3 = pwd + "/eigen-3.4-rc1/"
			print("EIGEN3 is %s." % EIGEN3)
		PYBIND11 = subprocess.run("pip show pybind11 | grep 'Location:'", capture_output=True, text=True, shell=True).stdout.strip().split()[1] + "/pybind11/include/"
		print("PYBIND11 is %s." % PYBIND11)

		# Configuring the makefile
		subprocess.check_call(["sed", "-i", "s/__MAKE__/" + MAKE.replace('/', "\/") + "/g", "makefile"])
		subprocess.check_call(["sed", "-i", "s/__CXX__/" + CXX.replace('/', "\/") + "/g", "makefile"])
		subprocess.check_call(["sed", "-i", "s/__AR__/" + AR.replace('/', "\/") + "/g", "makefile"])
		subprocess.check_call(["sed", "-i", "s/__PYTHON3__/" + PYTHON3.replace('/', "\/") + "/g", "makefile"])
		subprocess.check_call(["sed", "-i", "s/__EIGEN3__/" + EIGEN3.replace('/', "\/") + "/g", "makefile"])
		subprocess.check_call(["sed", "-i", "s/__PYBIND11__/" + PYBIND11.replace('/', "\/") + "/g", "makefile"])

		# Make
		nproc = subprocess.run("nproc", capture_output=True, text=True).stdout.strip()
		subprocess.check_call(["sed", "-i", "s/__OBJ__/__CPP__/g", "makefile"])
		subprocess.check_call([MAKE, "-j", nproc])
		subprocess.check_call(["sed", "-i", "s/__CPP__/__PYTHON__/g", "makefile"])
		subprocess.check_call([MAKE, "-j", nproc])

		super().run()


setup(
		name = "Maniverse",
		author = "FreemanTheMaverick",
		description = "Function optimization on manifolds",
		version = "0.2.1",
		url = "https://github.com/FreemanTheMaverick/Maniverse.git",
		packages = find_packages('src'),
		package_data = { "src": ["lib/*"] },
		cmdclass = { "build": CustomBuild },
		classifiers = ["Programming Language :: Python :: 3"]
)
