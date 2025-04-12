from setuptools import setup, find_packages

setup(
    name="timesheet_common_timesheet_mfdenison_hopkinsep",
    version="0.0.3",
    author="Mathew Denison",
    description="Common models and utilities for Timesheet management",
    packages=find_packages(),  # Finds pto_common and all its subpackages automatically.
    install_requires=[
        "sqlmodel>=0.0.6",
        "pydantic",
    ],
)
