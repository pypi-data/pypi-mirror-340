import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

setup(
    name = 'serendipity_matrix',
    version = '1.0.2',
    author = 'Jesús S. Aguilar-Ruiz, Alejandro García Conde',
    #author_email=,
    description = 'Serendipity Matrix',
    long_description = (HERE / "README.md").read_text(encoding='utf-8'), 
    long_description_content_type = "text/markdown",
    #url=,
    packages=["serendipity_matrix"],
    # classifiers=,
    # python_requires=,
    install_requires = ["numpy","pandas","matplotlib"],
    license = "BSD 3-Clause License"
)