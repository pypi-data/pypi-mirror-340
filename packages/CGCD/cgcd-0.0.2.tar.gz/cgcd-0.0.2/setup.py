from setuptools import setup, find_packages

setup(
    name="CGCD",
    version="0.0.2",
    author="JF Benavente, JE Tenopala",
    author_email="jf.benavente@ciemat.es, jtenopalap1800@alumno.ipn.mx",
    description="Computer Glow Curve Deconvolution",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JFBenavente/CGCD",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
    "numpy", "pandas", "matplotlib", "scipy", "plotly", "openpyxl"
    ],
    include_package_data=True,
    license="MIT",
)
