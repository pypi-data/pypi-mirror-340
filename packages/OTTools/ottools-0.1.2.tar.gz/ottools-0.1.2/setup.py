from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    description = fh.read()

setup(
    name='OTTools',  # Use a unique name here
    version='0.1.2',
    description='A Python package for Linear Programming and Transportation Problems',
    long_description=description,
    long_description_content_type='text/markdown',
    author='Mohammad Saad Nathani,Pranav Mundhra',
    author_email='saadnathani2005@gmail.com,pranavmundhara2005@gmail.com',
    url='https://github.com/Strangehumaan/OT',  # optional
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'plotly',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
