from setuptools import find_packages, setup

# Read the contents of the README file
with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='sif_tools',  
    version='0.3.2', 
    author='Bjorn F. Schroder N.', 
    author_email='Bjornfschroder@gmail.com',  
    description='A light-weight package for Andor SIF file analysis', 
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BjornFS/SIF-Tools', 
    packages=find_packages(), 
    classifiers=[
        'Programming Language :: Python :: 3', 
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
    install_requires=[
        'matplotlib',
        'numpy',  
        'scipy',
    ],
    entry_points={
        'console_scripts': [
            'sif-tools=sif_tools.__main__:main',
        ],
    },
)

#new version:
## change version number in setup.py
## python setup.py sdist bdist_wheel
## twine upload dist/* 