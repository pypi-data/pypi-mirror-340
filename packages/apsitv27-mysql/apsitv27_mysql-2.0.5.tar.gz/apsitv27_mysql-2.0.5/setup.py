from setuptools import setup, find_packages

setup(
    name="apsitv27-mysql",
    version="2.0.5",  # Incremented version
    description="MySQL Database Server Manager with persistent storage",
    author="apsitv27",
    author_email="23104195@apsit.edu.in",
    url="https://github.com/apsitv27/apsitv27-mysql",
    packages=find_packages(),
    include_package_data=True,  # Important for MANIFEST.in
    entry_points={
        "console_scripts": [
            "apsitv27-mysql=apsitv27_mysql.main:build_and_run_mysql_container"
        ],
    },
    install_requires=[
        "docker",
        "setuptools>=65.0.0",
    ],
    # Explicitly define package data
    package_data={
        "apsitv27_mysql": ["Dockerfile", "entrypoint.sh"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
