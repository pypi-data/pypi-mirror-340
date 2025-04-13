from setuptools import setup, find_packages

setup(
    name="IA23005UNO",
    version="0.1.0",
    packages=['IA23005UNO'],
    author="Rubén Iglesias IA23005",
    author_email="rubenedgardo70080503@gmail.com",
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RubenIglesias1F20/IA23005UNO",
    download_url="",
    license='MIT',
    install_requires=[
        "numpy>=1.20.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
