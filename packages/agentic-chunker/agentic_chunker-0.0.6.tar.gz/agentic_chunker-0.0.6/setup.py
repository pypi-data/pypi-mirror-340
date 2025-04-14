from setuptools import setup, find_packages
from pathlib import Path

with open("README.md", "r") as f:
    long_description = f.read()

version_file = Path(__file__).parent / "agentic_chunker/version.py"
exec(version_file.read_text())

setup(
    name='agentic_chunker',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'openai>=1.24.1',
        'tqdm>=4.11.1',
    ],
    description="A tool for improving the quality of chunks.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gurram Siddarth Reddy',
)