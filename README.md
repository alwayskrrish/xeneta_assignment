# Rate Calculator API Deployment Guide

This guide provides step-by-step instructions to deploy the Rate Calculator FastAPI application.

## Prerequisites

1. **Linux Machine**: Ensure you have a Linux-based operating system.
2. **Python 3.8+**: Install Python 3.8 or later.
3. **Git**: Ensure Git is installed.
4. **Docker**: Install Docker to containerize the application.
5. **PostgreSQL**: Install PostgreSQL if not using Docker for the database.

## Steps

### 1. Clone the Repository

Clone the Rate Calculator repository from your version control system (e.g., GitHub).

```bash
git clone https://github.com/alwayskrrish/xeneta_assignment.git
cd xeneta_assignment
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root directory and define the necessary environment variables:

```env
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_HOSTNAME=your_db_hostname
DB_DATABASE=your_db_name
DB_PORT=5432
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

```bash
source .env
```

### 3. Create a Virtual Environment

Create and activate a Python virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install the dependencies

Install the required Python dependencies.

```bash
pip3 install -r requirements.txt
```

### 5. Run the FastAPI Application

To start the FastAPI application, execute the following command:

```bash
python3 src/main.py --host 0.0.0.0 --port 8000 
```

or 

## Deploy using docker

You can execute the provided Dockerfile by running:


```bash
docker build -t ratestask .
```

This will create a container with the name *ratestask*, which you can
start in the following way:

```bash
docker run -p 0.0.0.0:8000:8000 --name ratestask ratestask
```