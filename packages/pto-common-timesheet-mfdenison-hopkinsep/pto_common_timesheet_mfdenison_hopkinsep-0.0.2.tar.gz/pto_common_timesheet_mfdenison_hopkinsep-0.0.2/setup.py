from setuptools import setup, find_packages

setup(
    name="pto_common_timesheet_mfdenison_hopkinsep",
    version="0.0.2",
    author="Mathew Denison",
    description="Common models and utilities for PTO management",
    packages=find_packages(),  # Finds pto_common_timesheet_mfdenison_hopkinsep and all its subpackages automatically.
    install_requires=[
        "sqlmodel>=0.0.6",
        "pydantic",
    ],
)
