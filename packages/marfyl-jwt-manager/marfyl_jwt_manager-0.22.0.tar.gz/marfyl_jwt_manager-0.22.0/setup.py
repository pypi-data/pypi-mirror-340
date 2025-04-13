from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='marfyl_jwt_manager',
    version='0.22.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='A service to process jwt from headers',
    author='Eduardo Ponce',
    author_email='poncejones@gmail.com',
    packages=find_packages(),
    install_requires=[
        'PyJWT',
        'cryptography',
        'fastapi',
        'starlette',
        'python-dotenv'
    ],
    python_requires='>=3.9',
)