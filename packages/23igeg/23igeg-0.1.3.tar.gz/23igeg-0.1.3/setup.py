from setuptools import setup, find_packages

setup(
    name="23igeg",
    version="0.1.3",
    author="Il Tuo Nome",
    description="Libreria dimostrativa di keylogging per progetti di sicurezza informatica",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tuo-user/23igeg",
    packages=find_packages(include=["igeg", "igeg.*"]),
    install_requires=[
        "pynput"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Education",
    ],
    python_requires='>=3.6',
)
