from setuptools import setup, find_packages

setup(
    name='Counter-Strike 1.6 AIAIMBOT',
    version='0.1.0',
    author='TGrozdanovski',
    description='AI aimbot for Counter-Strike 1.6',
    packages=find_packages(),
    install_requires=[
        'torch==2.1.2',
        'opencv_python==4.7.0.72',
        'numpy==1.26.3',
        'PyAutoGUI==0.9.54',
        'PyGetWindow==0.0.9',
        'mss==9.0.1',
        'keyboard==0.13.5',
        'pywin32==306'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
