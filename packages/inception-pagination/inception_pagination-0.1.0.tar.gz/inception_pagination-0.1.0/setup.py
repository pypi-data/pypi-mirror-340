import os
from setuptools import setup, find_packages, Command



class CleanUpCommand(Command):
    """Custom command to remove files created by inception_active_user."""

    description = "Clean up files created by inception_active_user"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        pass


setup(
    name="inception_pagination",
    version="0.1.0",
    author="KhaduaBloom",
    author_email="khaduabloom@gmail.com",
    description="inception_pagination is a package that allows you to paginate the data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KhaduaBloom/inceptionforcepackages/tree/main/PythonPackage/inceptionPagination",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13.0",
    install_requires=[
        "graypy==2.1.0",
        "psutil==6.1.0",
    ],
    cmdclass={
        "cleanup": CleanUpCommand,
    },
)
