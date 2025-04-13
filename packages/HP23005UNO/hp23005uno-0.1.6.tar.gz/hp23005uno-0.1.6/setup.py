from setuptools import setup, find_packages

readme = open("./README.md", "r")

setup(
    name="HP23005UNO",
    version="0.1.6",
    description="Librería para resolver ecuaciones lineales y no lineales con métodos numéricos",
    long_description=readme.read(),
    long_description_content_type="text/markdown",
    author="HP23005",
    author_email="hp23005@ues.edu.sv",
    url="https://github.com/HP23005/HP23005UNO",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.18",
        "scipy>=1.4"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    python_requires='>=3.7',
)
