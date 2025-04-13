from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README.md Mahamat
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='python_data-structures_bootcamp',
    version='0.1.2',
    description='This is my first try in building package',
    author='Mahamat Assouna',
    author_email='amahamat@aimsammi.org',
    packages=find_packages(),
    # install_requires=[
    #     'numpy',
    #     ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
    long_description=long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/Mahamat19/Mahamat_Data_Struct_Rep',
    license='MIT',
    
)
