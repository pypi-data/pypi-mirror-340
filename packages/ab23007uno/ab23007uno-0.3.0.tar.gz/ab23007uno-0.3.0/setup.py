from setuptools import setup


setup(
    name="ab23007uno",
    version="0.3.0",
    author="Katya Asencio",
    author_email="ab23007@ues.edu.sv",
    description="Librería de métodos numéricos para resolver problemas matemáticos",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KatyaAsencio/AB23007UNO",
    packages=["ab23007uno"],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
    ],
) 