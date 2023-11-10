# MaterialsDB Project

This project consists of a backend developed using Flask and a frontend using Bootstrap.

## Coverage

[![Coverage Status](https://coveralls.io/repos/github/msegal347/COMS_4111_Project/badge.svg?branch=main)](https://coveralls.io/github/msegal347/COMS_4111_Project?branch=main)


## Backend Setup

### Initialize the Conda Environment

1. Navigate to the backend directory and run the following command to create a Conda environment:
    ```bash
    conda env create -f environment.yml
    ```
2. Activate the environment:
    ```bash
    conda activate materialsDB
    ```

### Install Python Dependencies

Run the following command to install the necessary Python packages:

```bash
pip install -r requirements.txt
```

### Running Tests

To run the tests, run the following command:

```bash
pytest
```

```bash
set PYTHONPATH=D:\School\Intro_to_Databases\DB_Project\COMS_4111_Project\backend
```

### Linting and Formatting

To check for linting issues:

```bash
flake8
```

To check for formatting issues:

```bash
black --check .
```

To fix formatting issues:

```bash
black .
```

## Frontend Setup

### Install Node.s and npm
If you don't have Node.js and npm installed, download and install them from here: https://nodejs.org/en

### Install Project Dependencies

Navigate to the drontend directory and run:

```bash
npm install
```

This will install all the dependencies listed in package.json.

### Running tests

To run the front-end tests, run the following command:

```bash
npm test
```

### Linting and Formatting

To check for linting issues:

```bash
npm run lint
```

To fix linting issues:

```bash
npm run lint:fix
```

To check for formatting issues:

```bash
npm run prettier
```

To fix formatting issues:

```bash
npm run prettier:fix
```

### Accessing the Docker Database

To access the database, run the following command:

```bash
docker exec -it docker-db-1 /bin/bash
```

Then, run the following command to access the database:

```bash
psql -U username database_name
```

If running into a collation error, run the following command:

```bash
ALTER DATABASE "materialsDB" REFRESH COLLATION VERSION;
```