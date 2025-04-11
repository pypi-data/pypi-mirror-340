from setuptools import setup, find_packages

setup(
    name='danielle_data_structures_python',
    version='0.1.0',
    author='Danielle Kapsa',
    description='A Python package to manage basic data structures like arrays, stacks, queues, and lists.',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dany237/data-structures-python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
