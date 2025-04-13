from setuptools import setup, find_packages

setup(
    name="apsitv27-mysql",
    version="2.0.0",  # Updated version to 2.0.0
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
)
