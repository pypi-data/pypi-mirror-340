from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="MG23117UNO",
    version="0.1.2",
    author="Kevin Martínez",
    author_email="mg23117@ues.edu.sv",
    description="Resolución de sistemas de ecuaciones con algunos métodos matematicos conocidos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mg23117/MG23117UNO",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["numpy>=1.24"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)