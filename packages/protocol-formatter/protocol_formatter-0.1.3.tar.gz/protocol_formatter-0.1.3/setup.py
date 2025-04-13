from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="protocol_formatter",
    version="0.1.3",
    author="Prakash Babu Adhikari",
    author_email="pbadhikari@yahoo.com",
    description="A utility to format raw text protocols into styled PDFs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adhikaripb/protocol_formatter",
    packages=find_packages(),
    entry_points={"console_scripts": ["protocol_formatter=protocol_formatter.__main__:main"]},
    include_package_data=True,
    install_requires=[
        "python-docx",
        "fpdf",
        "svgwrite",
        "cairosvg",
    ],
    package_data={
        "protocol_formatter": ["*.png"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
