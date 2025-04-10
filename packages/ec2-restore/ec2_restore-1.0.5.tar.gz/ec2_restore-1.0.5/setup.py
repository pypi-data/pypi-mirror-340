from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ec2-restore",
    version="1.0.5",
    author="Jyothish Kshatri",
    author_email="kshatri.jyothish3@gmail.com",
    description="A tool for restoring EC2 instances from AMIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jyothishkshatri/ec2-restore",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'ec2_restore': ['*.yaml'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "boto3>=1.26.0",
        "rich>=10.0.0",
        "pyyaml>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ec2-restore=ec2_restore.modules.cli:cli",
        ],
    },
) 