from setuptools import find_packages, setup

setup(
    name="flask_inputfilter",
    version="0.3.0",
    license="MIT",
    author="Leander Cain Slotosch",
    author_email="slotosch.leander@outlook.de",
    description="A library to easily filter and validate input data in "
    "Flask applications",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/LeanderCS/flask-inputfilter",
    packages=find_packages(
        include=["flask_inputfilter", "flask_inputfilter.*"]
    ),
    install_requires=[
        "flask>=2.1",
        "typing_extensions>=3.6.2",
    ],
    extras_require={
        "optional": [
            "pillow>=8.0.0",
            "requests>=2.22.0",
        ],
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.7",
    project_urls={
        "Documentation": "https://leandercs.github.io/flask-inputfilter",
        "Source": "https://github.com/LeanderCS/flask-inputfilter",
    },
)
