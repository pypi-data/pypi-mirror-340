from setuptools import setup, find_packages

setup(
    name="adrishyam",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "pillow>=10.0.0",
        "matplotlib>=3.7.0",
        "scipy>=1.10.0",
    ],
    author="Krushna Parmar, Saumya Gohil",
    author_email="parmarkrushna7@gmail.com, gohilsaumya16@gmail.com",
    description="A Python package for image dehazing using Dark Channel Prior",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Krushna-007/adrishyam",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.8",
    keywords="image-processing dehazing dark-channel-prior computer-vision",
) 