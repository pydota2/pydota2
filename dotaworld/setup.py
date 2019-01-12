import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dotaworld",
    version="0.1.2",
    author="Andrzej Gorski",
    author_email="nostrademous@hotmail.com",
    description="dotaworld is a framework for tracking/interpreting Dota2 protobuf data in internal class objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pydota2/pydota2/dotaworld",
    packages=setuptools.find_packages(),
    package_data={'dotaworld': ['lua/*.lua']},
    python_requires='>=3.7',
    classifiers=[
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: Freeware",
        "License :: Other/Proprietary License",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
    ],
    install_requires=[
        'protobuf',
    ],
    extras_require={
    },
)
