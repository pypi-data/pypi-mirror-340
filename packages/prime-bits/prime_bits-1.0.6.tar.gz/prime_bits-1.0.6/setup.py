from setuptools import setup, find_packages

setup(
    name="prime_bits",
    version="1.0.6",
    author="Zikithezikit",
    author_email="zikithezikit@example.com",
    description="A package to get prime numbers from bits.",
    license="MIT",
    keywords="prime number bits large",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Zikithezikit/prime_bits",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
    ],
)