# Order, an Order Management Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
![Coverage](./coverage.svg)
## Overview

The **Order Management Service** is a RESTful API built with Flask, designed to handle orders and their associated items. It provides endpoints to create, read, update, and delete orders and items, making it suitable for e-commerce platforms, inventory systems, and other applications requiring order management functionality.

## Features

- **Order Management**: Create, retrieve, update, and delete orders.
- **Item Management**: Add, list, retrieve, and remove items associated with orders.
- **Database Integration**: Utilizes PostgreSQL with SQLAlchemy ORM for data persistence.
- **Testing Suite**: Comprehensive tests using `unittest` and `factory_boy`.
- **CLI Commands**: Manage database operations via Flask CLI.
- **Development Environment**: Configured with VSCode Dev Containers for consistent development setups.
- **Logging**: Configured logging for monitoring and debugging.

## Technologies Used

- **Programming Language**: Python
- **Framework**: Flask
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Testing**: `unittest`, `factory_boy`
- **Containerization**: Docker, VSCode Dev Containers
- **Additional Libraries**: `click`, `flask_sqlalchemy`, `factory_fuzzy`

## Installation and Setup

### Prerequisites

- **Docker**: Installed and running on your machine.
- **VSCode**: With the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
- **Python**: Version 3.11 or higher (if not using Dev Containers).
- **PostgreSQL**: Ensure PostgreSQL is installed and running.
- **git**: For cloning the repository.

### Using VSCode Dev Containers

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-repo/order-management-service.git
    cd order-management-service
    ```

2. **Open in VSCode**

    Open the cloned repository in Visual Studio Code.

3. **Reopen in Container**

    Press `F1` and select **Remote-Containers: Reopen in Container**. This will build the Docker environment as specified in `.devcontainer/devcontainer.json`.

4. **Post-Installation Setup**

    The `post-install.sh` script will run automatically to set up additional tools and configurations inside the container.


## Configuration

Configuration parameters are managed in the `service/config.py` file and can be set via environment variables.

- **DATABASE_URI**: Connection string for PostgreSQL.
- **SECRET_KEY**: Secret key for session management.
- **LOGGING_LEVEL**: Logging verbosity level.

## Usage

### Running the Service

Start the Flask development server:

```bash
flask run
```

The service will be accessible at `http://127.0.0.1:8080/`. You can edit the port in `.flaskenv`.

### API Endpoints

#### Order Endpoints

- **Create Order**

    - **URL**: `/orders`
    - **Method**: `POST`
    - **Body**: JSON object containing order details.
    - **Response**: Created order object with `201 Created` status.

- **List All Orders**

    - **URL**: `/orders`
    - **Method**: `GET`
    - **Response**: List of all orders sorted by date in descending order with `200 OK` status.

- **Update Order**

    - **URL**: `/orders/<order_id>`
    - **Method**: `PUT`
    - **Body**: JSON object with updated order details.
    - **Response**: Updated order object with `200 OK` status.

- **Delete Order**

    - **URL**: `/orders/<order_id>`
    - **Method**: `DELETE`
    - **Response**: Empty body with `204 No Content` status.

#### Item Endpoints

- **Create Item**

    - **URL**: `/orders/<order_id>/items`
    - **Method**: `POST`
    - **Body**: JSON object containing item details.
    - **Response**: Created item object with `201 Created` status.

- **List Items for an Order**

    - **URL**: `/orders/<order_id>/items`
    - **Method**: `GET`
    - **Response**: List of items for the specified order with `200 OK` status.

- **Retrieve Item**

    - **URL**: `/orders/<order_id>/items/<product_id>`
    - **Method**: `GET`
    - **Response**: Item object with `200 OK` status.

- **Delete Item**

    - **URL**: `/orders/<order_id>/items/<product_id>`
    - **Method**: `DELETE`
    - **Response**: Empty body with `204 No Content` status.

### CLI Commands

- **Create Database**

    Recreate the local database tables.

    ```bash
    flask db-create
    ```

## Testing

### Running Tests

If using Dev Containers, tests can be run directly within the container. Otherwise, ensure your virtual environment is activated.

```bash
poetry run pytest
```

### Test Coverage

- **Model Tests**: Located in `tests/test_order.py` and `tests/test_item.py`.
- **Route Tests**: Located in `tests/test_routes.py`.
- **CLI Command Tests**: Located in `tests/test_cli_commands.py`.

## Project Structure

```
order-management-service/
├── .devcontainer/
│   ├── devcontainer.json         # Dev Container configuration
│   ├── Dockerfile                # Dockerfile for the development environment
│   └── scripts/
│       ├── install-tools.sh       # Script to install development tools
│       └── post-install.sh        # Post-installation setup script
├── service/
│   ├── __init__.py                # Application factory
│   ├── config.py                  # Configuration parameters
│   ├── models/
│   │   ├── __init__.py            # Model package initializer
│   │   ├── item.py                # Item model
│   │   ├── order.py               # Order model
│   │   └── persistent_base.py     # Base model with CRUD operations
│   ├── routes.py                  # API route definitions
│   └── common/
│       ├── cli_commands.py        # CLI commands for Flask
│       ├── error_handlers.py      # Error handling
│       ├── log_handlers.py        # Logging setup
│       └── status.py              # HTTP status codes
├── tests/
│   ├── __init__.py                # Test package initializer
│   ├── factories.py               # Factory Boy factories for testing
│   ├── test_cli_commands.py       # CLI command tests
│   ├── test_item.py               # Item model tests
│   ├── test_order.py              # Order model tests
│   └── test_routes.py             # Route tests
├── pyproject.toml                 # Poetry configuration
├── poetry.lock                    # Poetry lock file
├── requirements.txt               # Python dependencies (if applicable)
├── docker-compose.yml             # Docker Compose configuration
├── .env                           # Environment variables (to be created)
├── .gitignore                     # Git ignore rules
├── README.md                      # Project documentation
└── .flaskenv                      # Flask environment variables
```

## Development Environment

### VSCode Dev Containers

This project is configured to use VSCode Dev Containers for a consistent development environment.

- **Dev Container Configuration**: Located in `.devcontainer/devcontainer.json`.
- **Scripts**:
    - `install-tools.sh`: Installs necessary development tools inside the container.
    - `post-install.sh`: Performs post-installation setup, such as configuring Git and aliases.

### Docker

The project leverages Docker for containerization, ensuring that all developers work in the same environment.

- **Dockerfile**: Sets up the Python environment and installs dependencies using Poetry.
- **Docker Compose**: Manages multi-container applications, if applicable.

## License

Licensed under the [Apache License 2.0](https://opensource.org/licenses/Apache-2.0).

## Acknowledgements

This project is part of the New York University (NYU) master's class: **CSCI-GA.2820-001 DevOps and Agile Methodologies**, created and taught by [John J. Rofrano](https://cs.nyu.edu/~rofrano/).

