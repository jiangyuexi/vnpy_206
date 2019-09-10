"""
vn.py - By Traders, For Traders.

The vn.py project is an open-source quantitative trading framework
that is developed by traders, for traders.

The project is mainly written in Python and uses C++ for low-layer
and performance sensitive infrastructure.

Using the vn.py project, institutional investors and professional
traders, such as hedge funds, prop trading firms and investment banks,
can easily develop complex trading strategies with the Event Engine
Strategy Module, and automatically route their orders to the most
desired destinations, including equity, commodity, forex and many
other financial markets.
"""

import ast
import os
import platform
import re
import sys

from setuptools import Extension, find_packages, setup

with open("vnpy/__init__.py", "rb") as f:
    version_line = re.search(
        r"__version__\s+=\s+(.*)", f.read().decode("utf-8")
    ).group(1)
    version = str(ast.literal_eval(version_line))

if platform.uname().system == "Windows":
    compiler_flags = [
        "/MP", "/std:c++17",  # standard
        "/O2", "/Ob2", "/Oi", "/Ot", "/Oy", "/GL",  # Optimization
        "/bigobj",  # Better compatibility
        "/wd4819",  # 936 code page
        "/D_CRT_SECURE_NO_WARNINGS",  # suppress warning of unsafe functions like fopen, strcpy, etc
    ]
    extra_link_args = []
    runtime_library_dirs = None
else:
    compiler_flags = [
        "-std=c++17",  # standard
        "-O3",  # Optimization
        "-Wno-delete-incomplete", "-Wno-sign-compare",
    ]
    extra_link_args = ["-lstdc++"]
    runtime_library_dirs = ["$ORIGIN"]


def gather_autocxxpy_generated_files(root: str):
    fs = [os.path.join(root, "module.cpp")]
    for root, dirs, filenames in os.walk(root):
        for filename in filenames:
            filebase, ext = os.path.splitext(filename)
            if ext == ".cpp" and filebase.startswith("generated_functions_"):
                path = os.path.join(root, filename)
                fs.append(path)
    return fs


vnctpmd = Extension(
    "vnpy.api.ctp.vnctpmd",
    [
        "vnpy/api/ctp/vnctp/vnctpmd/vnctpmd.cpp",
    ],
    include_dirs=["vnpy/api/ctp/include",
                  "vnpy/api/ctp/vnctp", ],
    define_macros=[],
    undef_macros=[],
    library_dirs=["vnpy/api/ctp/libs", "vnpy/api/ctp"],
    libraries=["thostmduserapi_se", "thosttraderapi_se", ],
    extra_compile_args=compiler_flags,
    extra_link_args=extra_link_args,
    runtime_library_dirs=runtime_library_dirs,
    depends=[],
    language="cpp",
)
vnctptd = Extension(
    "vnpy.api.ctp.vnctptd",
    [
        "vnpy/api/ctp/vnctp/vnctptd/vnctptd.cpp",
    ],
    include_dirs=["vnpy/api/ctp/include",
                  "vnpy/api/ctp/vnctp", ],
    define_macros=[],
    undef_macros=[],
    library_dirs=["vnpy/api/ctp/libs", "vnpy/api/ctp"],
    libraries=["thostmduserapi_se", "thosttraderapi_se", ],
    extra_compile_args=compiler_flags,
    extra_link_args=extra_link_args,
    runtime_library_dirs=runtime_library_dirs,
    depends=[],
    language="cpp",
)
vnoes = Extension(
    name="vnpy.api.oes.vnoes",
    sources=gather_autocxxpy_generated_files(
        "vnpy/api/oes/vnoes/generated_files/",
    ),
    include_dirs=["vnpy/api/oes/vnoes/include",
                  "vnpy/api/oes/vnoes/include/oes", ],
    define_macros=[("BRIGAND_NO_BOOST_SUPPORT", "1")],
    undef_macros=[],
    library_dirs=["vnpy/api/oes/vnoes/libs"],
    libraries=["oes_api"],
    extra_compile_args=compiler_flags,
    extra_link_args=extra_link_args,
    runtime_library_dirs=runtime_library_dirs,
    depends=[],
    language="cpp",
)

if platform.system() == "Windows":
    # use pre-built pyd for windows ( support python 3.7 only )
    ext_modules = []
elif platform.system() == "Darwin":
    ext_modules = []
else:
    ext_modules = [vnctptd, vnctpmd]


def check_extension_build_flag(key: str, module: Extension):
    value = os.environ.get(key, None)
    if value is not None:
        global ext_modules
        if value == '1':
            ext_modules = list(set(ext_modules) | {module})
        elif value == '0':
            ext_modules = list(set(ext_modules) - {module})
        else:
            raise ValueError(f"Flag {key} should be '0' or '1', but {repr(value)} got.")


check_extension_build_flag("VNPY_BUILD_OES", vnoes)


pkgs = find_packages()


def is_psycopg2_exists():
    try:
        import psycopg2  # noqa
        return True
    except ImportError:
        return False


install_requires = [
    "PyQt5",
    "qdarkstyle",
    "requests",
    "websocket-client",
    "peewee",
    "pymysql",
    "mongoengine",
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "futu-api",
    "tigeropen",
    "rqdatac",
    "ta-lib",
    "ibapi",
    "deap"
]
if not is_psycopg2_exists():
    install_requires.append("psycopg2-binary")

if sys.version_info.minor < 7:
    install_requires.append("dataclasses")

setup(
    name="vnpy",
    version=version,
    author="vn.py team",
    author_email="vn.py@foxmail.com",
    license="MIT",
    url="https://www.vnpy.com",
    description="A framework for developing quant trading systems.",
    long_description=__doc__,
    keywords='quant quantitative investment trading algotrading',
    include_package_data=True,
    packages=pkgs,
    package_data={"": [
        "*.ico",
        "*.ini",
        "*.dll",
        "*.so",
        "*.pyd",
    ]},
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows Server 2008",
        "Operating System :: Microsoft :: Windows :: Windows Server 2012",
        "Operating System :: Microsoft :: Windows :: Windows Server 2012",
        "Operating System :: POSIX :: Linux"
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: Chinese (Simplified)"
    ],
    ext_modules=ext_modules
)
