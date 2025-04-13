from setuptools import setup, find_packages

setup(
    name="SAMIRTextEr",  
    version="0.2.0",  
    packages=find_packages(),  
    install_requires=[  
        "colorama",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  )
