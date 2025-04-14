from setuptools import setup, find_packages
import os

# Get the directory where setup.py is located
this_directory = os.path.abspath(os.path.dirname(__file__))

# Read the README.md file for long description
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ABD-model',
    version='0.3.0',
    author='Safi Ullah Majid',
    author_email='Safeullahmaid@gmail.com',
    description='YOLO-based model for atom and bond detection in molecular images.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Safi-ullah-majid/ABD-model',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'torch',
        'opencv-python',
        'numpy',
        'matplotlib',
        # Add additional dependencies if needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    package_data={
        'ABD_model': ['ABD.pt'],  # Ensure ABD.pt is included
    },
)
