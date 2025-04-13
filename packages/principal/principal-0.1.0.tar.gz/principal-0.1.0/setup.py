from setuptools import setup, find_packages

setup(
    name='principal',                     # Your package name
    version='0.1.0',                    # Version
    description='Principal Component Analysis(PCA)',
    author='Aryan Bhagwat',
    author_email='legendasur531@gmail.com',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
