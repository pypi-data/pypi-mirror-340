from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="imagem_processing_frr",
    version="0.0.1",
    author="faustoramos",
    author_email="faustorobert@hotmail.com",
    description="Permite comparar duas imagens e gerar uma terceira imagem que destaca as diferencas em preto e branco.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/faustorramos/image-processing-pypi/",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.7',
)
