# INSTALL OR USE MYSQL THROUGH apsitv27-mysql

### Prerequisites

#### Before running the module, ensure the following:

**Docker Installation** 
Docker must be installed and running on your system.

To check if Docker is installed:

Run the following command:

```bash
docker --version
```
If Docker is not installed, download and install Docker for your operating system.


#### Start Docker:

**On Windows:**
Open the Docker Desktop application manually 

**On Ubuntu/Linux:**
Start the Docker service using:
```bash

sudo systemctl start docker
```
Ensure Docker is Running

## Installation
To install the ```apsitv27-mysql``` module:

```bash
pip install apsitv27-mysql
```
### Usage
Once installed, you can start the MySQL server by simply running:
```bash
apsitv27-mysql
```
This command will:

- Build a Docker container with a MySQL server.

- Automatically manage persistent data storage using Docker volumes (mysql_data), ensuring that your database remains intact even after container restarts.

- Launch an interactive MySQL shell for SQL practice.


Clearing Data:
If you want to start fresh and remove all stored data:

```bash
docker volume rm mysql_data
```
