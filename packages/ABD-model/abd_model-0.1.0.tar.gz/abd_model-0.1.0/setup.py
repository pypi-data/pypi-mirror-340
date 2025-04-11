from setuptools import setup, find_packages

setup(
    name='ABD-model',
    version='0.1.0',
    author='Safi Ullah Majid',
    author_email='your-email@example.com',
    description='YOLO-based model for atom and bond detection in molecular images.',
    long_description=open(r'C:\Users\Safi Ullah Majid\Desktop\AI Projects\process Data\500\model\PyPl\README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Safi-ullah-majid/ABD-model',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'torch',
        'opencv-python',
        'numpy',
        'matplotlib',
        # Add other requirements from requirements.txt if needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

