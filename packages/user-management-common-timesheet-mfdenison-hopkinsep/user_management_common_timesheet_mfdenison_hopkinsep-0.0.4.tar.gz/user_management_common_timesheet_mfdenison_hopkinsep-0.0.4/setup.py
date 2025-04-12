from setuptools import setup, find_packages

setup(
    name="user_management_common_timesheet_mfdenison_hopkinsep",
    version="0.0.4",
    author="Mathew Denison",
    description="Common models and utilities for User management",
    packages=find_packages(),  # Finds pto_common and all its subpackages automatically.
    install_requires=[
        "sqlmodel>=0.0.6",
        "pydantic",
    ],
)
