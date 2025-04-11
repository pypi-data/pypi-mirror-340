from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyecutest",
    version="0.1.0",
    author="PyECUTest Team",
    author_email="your.email@example.com",
    description="A testing framework for ECU testing based on pytest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pyecutest",
    packages=find_packages(include=['*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "pytest>=7.0.0",
        "allure-pytest>=2.13.0",
        "cantools>=40.0.0",
        "python-can>=4.5.0",
        "niveristand>=3.2.0",
        "adbutils>=2.8.0",
        "pya2l>=0.1.4",
        "py_canoe>=3.0.2",
        "pymysql>=1.1.1",
        "uiautomator2>=3.2.2",
        "requests>=2.28.0",
        "pythonnet>=3.0.4",
        "watchdog>=5.0.3",
        "pyyaml>=6.0.2",
        "pandas>=1.5.0",
        "openpyxl>=3.0.0",
        "pytest-assume>=2.4.3",
        "pytest-csv>=3.0.0",
        "psutil>=6.1.0",
        "pytest-repeat>=0.9.3",
        "intelhex>=2.3.0",
        "pyecharts>=2.0.7",
        "pytest-sugar>=1.0.0",
        "pywin32>=308",
        "a2lparser>=0.1.0,<1.0.0"
    ],
    extras_require={
        'a2l': [
            'a2lparser>=0.1.0,<1.0.0'
        ]
    },
    dependency_links=[
        "https://test.pypi.org/simple/a2lparser/"
    ],
    entry_points={
        "console_scripts": [
            "pyecutest=pyecutest.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "*.json",
            "*.yaml",
            "*.xlsx",
            "*.py",
            "databases/*/*",
            "config/*",
            "resource/*",
            "doc/*",
            "log/*",
            "report/*",
            "tests/*"
        ],
    },
) 