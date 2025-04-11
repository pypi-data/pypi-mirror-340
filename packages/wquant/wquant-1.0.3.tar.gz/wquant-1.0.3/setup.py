from pathlib import Path

from setuptools import setup, find_packages


def parse_requirements(file_path):
    """读取 requirements.txt 并返回列表"""
    requirements = []
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                requirements.append(line)
    return requirements


setup(
    name="wquant",
    version="1.0.3",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
)
