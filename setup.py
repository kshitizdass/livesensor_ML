from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:

    requirement_list :List[str]=[]

    return requirement_list

setup(
    name='sensor',
    version="1.0.1",
    author="Kshitiz Dass",
    author_email="kshitiz.dass@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements(),
)