# setup.py
from setuptools import setup, find_packages

setup(
    name="lprof_ext",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "libcst>=1.0.0",
        "line_profiler>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "lprof_ext=lprof_ext.cli:main",
        ],
    },
    author="Ruprof",
    description="A Python script profiler using @profile decorators",
    python_requires=">=3.8",
)