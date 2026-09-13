'''
The setup.py file is an essential part of package and 
distribution python project.It is used by setuptools 
(or distutils in older python versions) to define the
configuration of your projects, such as its metadata,
dependencies and more


'''



from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    this function  will written list of requirements
    """
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            #Read lines from the file
            lines=file.readlines()
            ## Process each line
            for line in lines:
                requirement=line.strip()
                ##ignore the empty line ans -e.
                if requirement and requirement!='-e.':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file not found")


    return requirement_lst

from setuptools import setup

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Megha Ambule",
    auther_email="ambulemegha15@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)