from setuptools import setup, find_packages

setup(
    name="count-bytes",               # Name on PyPI
    version="0.0.0a",                  # The 'a' at the end of 0.0.0a stands for alpha
    packages=find_packages(),
    install_requires=[
        "emoji>=2.0.0"
    ],             # Dependencies, if any
    author="Adonis Miclea",
    author_email="tilik_87@yahoo.com",
    description="A Python module that prints how many bytes are in a string or file",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
