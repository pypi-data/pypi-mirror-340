from setuptools import setup, find_packages

setup(
    name="apsitv27-mysql",
    version="2.0.2",
    description="MySQL Database Server Manager with persistent storage",
    author="apsitv27",
    author_email="23104195@apsit.edu.in",
    url="https://github.com/apsitv27/apsitv27-mysql",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "apsitv27-mysql=apsitv27_mysql.main:build_and_run_mysql_container"
        ],
    },
    install_requires=[
        "docker",
        "setuptools>=65.0.0",
    ],
    package_data={
        "apsitv27_mysql": ["Dockerfile", "dockerfile", "entrypoint.sh", "install_docker.sh", "install_docker.bat"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
