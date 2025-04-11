from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='arvd_ap',
    version='0.2.0',  # Incremented version
    packages=find_packages(),
    install_requires=[
    ],
    author='ARAVIND SREE U',
    author_email='uaravindsree@gmail.com',
    description='My description will help you to pass time and understand my ability of writing codes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AravindSreeU/arvd_ap',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
