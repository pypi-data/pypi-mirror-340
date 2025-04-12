from setuptools import setup, find_packages

setup(
    name='pypi_ci_package',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        "twine",
    ],
    entry_points={
        'console_scripts': [
            'cli=src.cli:main',
        ],
    },
)
