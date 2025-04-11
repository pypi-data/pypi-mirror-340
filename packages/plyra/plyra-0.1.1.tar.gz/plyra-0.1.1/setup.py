from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_descriptions = f.read()

setup(
    name="plyra",
    version="0.1.1",
    description="A modern, one-liner visualization library built on top of Plotly",
    long_description=long_descriptions,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Unknownuserfrommars",
    author_email="kev1511@gmail.com",
    url="https://github.com/Unknownuserfrommars/ProjectPlyra",
    packages=find_packages(),
    install_requires=[
        "plotly>=6.0.0",
        "pandas>=2.0.0",
        "numpy>=2.0.0",
        "scipy>=1.12.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    python_requires='>=3.10',
)
