import os
import subprocess
from setuptools import setup, find_packages, Command

class MakeBuild(Command):
    description = "Build the C++ shared library using Makefile"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Run make in the CO2Ne directory.
        cwd = os.path.join(os.path.dirname(__file__), "CO2Ne")
        subprocess.check_call(["make", "clean"], cwd=cwd)
        subprocess.check_call(["make"], cwd=cwd)

# Read the README for the long description.
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="molecule_potential",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for computing molecular potential energy using a C++ backend.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # Include the shared library in the package.
        "molecule_potential": ["../CO2Ne/libCO2Ne.so"],
    },
    cmdclass={
        "build_ext": MakeBuild,  # Runs the MakeBuild command before build_ext.
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires=">=3.6",
)