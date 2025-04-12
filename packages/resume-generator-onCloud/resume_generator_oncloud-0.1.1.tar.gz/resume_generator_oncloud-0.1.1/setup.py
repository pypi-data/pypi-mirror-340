from setuptools import setup, find_packages

setup(
    name="resume_generator_onCloud",
    version="0.1.1",
    description="It's a python library used to create a resume-generator on cloud",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["django>=4.0"],
)