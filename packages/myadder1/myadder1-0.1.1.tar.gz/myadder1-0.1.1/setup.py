from setuptools import setup, find_packages

setup(
    name='myadder1',                     # Your package name
    version='0.1.1',                    # Version
    description='A simple addition module that sums a list of numbers',
    author='Aryan Bhagwat',
    author_email='legendasur531@gmail.com',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
