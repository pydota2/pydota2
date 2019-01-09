import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydota2",
    version="0.1.0",
    author="Andrzej Gorski",
    author_email="nostrademous@hotmail.com",
    description="pydota2 is a framework to play Dota 2 leveraging Tim Zaman's dotaservice and dotaclient work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pydota2/pydota2",
    packages=setuptools.find_packages(),
    package_data={'pydota2': ['lua/*.lua']},
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
        'grpclib',
        'protobuf',
	'pprint',
	'torch',
	'tensorboardX',
	'aioamqp',
	'pika',
    ],
    extras_require={
        'dev': [
            'grpcio-tools',
        ],
	'distributed': [
            'google-cloud-storage',
	],
    },
)
