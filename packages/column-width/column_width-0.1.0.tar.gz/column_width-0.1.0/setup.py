from setuptools import setup, find_packages

setup(
    name="column-width",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'column-width=asciidoc_table_width_adjuster.main:main',
        ],
    },
    author="Puneet Bajaj",
    author_email="bajajpuneet223@gmail.com",
    description="A utility to adjust table column widths in AsciiDoc files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/column-width",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
