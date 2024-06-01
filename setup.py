from setuptools import find_packages, setup

# Read the contents of the README file
with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='sif_tools',  # Replace with your package name
    version='0.1.0',  # Initial version of your package
    author='Bjorn F. Schroder N.',  # Replace with your name
    author_email='Bjornfschroder@gmail.com',  # Replace with your email
    description='A light-weight package for Andor SIF file analysis',  # Brief description of the package
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BjornFS/SIF-Tools',  # Replace with the URL of your package's repository
    packages=find_packages(),  # Automatically find packages in the same directory
    classifiers=[
        'Programming Language :: Python :: 3',  # Supported Python version
        'License :: OSI Approved :: MPL-2.0',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version required
    install_requires=[
        'matplotlib',  # Include matplotlib
        'numpy',  # Include numpy
        'scipy', # Include scipy
    ],
)