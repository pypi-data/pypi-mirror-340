from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fundamentus_scraper",
    version="0.1.0",
    author="Seu Nome",
    author_email="seu@email.com",
    description="Web Scraper para dados do Fundamentus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seuusuario/fundamentus-scraper",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'beautifulsoup4>=4.9.3',
        'pandas>=1.2.0',
        'openpyxl>=3.0.7',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)