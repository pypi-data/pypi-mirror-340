from setuptools import setup, find_packages

setup(
    name="tabkan",
    version="0.1.2",
    author="Ali Eslamian",
    author_email="aseslamian@gmail.com",
    description="KAN-based neural architectures for tabular data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aseslamian/TAbKAN",  # Optional
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "torch>=2.0",
        "numpy>=1.22",
        "pandas",
        "tqdm",
        "scikit-learn",
        "optuna>=3.0",
        "fkan>=0.0.2",
        "rkan>=0.0.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)