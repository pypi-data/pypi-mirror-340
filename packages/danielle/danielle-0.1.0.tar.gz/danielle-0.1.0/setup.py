from setuptools import setup, find_packages

setup(
    name='danielle',  # This must be unique on PyPI
    version='0.1.0',
    author='Kapsa Danielle',
    author_email='adeandkofi@gmail.com',
    description='A Python package implementing core data structures from scratch',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dany237/data_structures',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
