# Order, an Order Management Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-FA24-003/orders/graph/badge.svg?token=EGJLN1OPQV)](https://codecov.io/gh/CSCI-GA-2820-FA24-003/orders)
![CI Build Status](https://github.com/SCI-GA-2820-FA24-003/orders/actions/workflows/workflow.yml/badge.svg)

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
    git clone https://github.com/CSCI-GA-2820-FA24-003/orders
    cd orders
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

---

## Data Model
### Order

- `id` (Integer): The unique identifier for the order.
- `date` (String): The date when the order was created in ISO format (`YYYY-MM-DD`).
- `status` (Integer): The status of the order.
- `amount` (Float): The total amount of the order.
- `address` (String): The shipping address for the order.
- `customer_id` (Integer): The identifier for the customer who placed the order.

### Item

- `product_id` (Integer): The unique identifier for the product.
- `order_id` (Integer): The identifier for the order to which the item belongs.
- `price` (Float): The price of the item.
- `quantity` (Integer): The quantity of the item ordered.

---

## Order REST API Service

This is a RESTful service for managing orders. You can create, read, update, and delete orders, as well as create, read, update, and delete items within orders.

### Table of Contents

- [Order, an Order Management Service](#order-an-order-management-service)
  - [Overview](#overview)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Installation and Setup](#installation-and-setup)
    - [Prerequisites](#prerequisites)
    - [Using VSCode Dev Containers](#using-vscode-dev-containers)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Running the Service](#running-the-service)
  - [Data Model](#data-model)
    - [Order](#order)
    - [Item](#item)
  - [Order REST API Service](#order-rest-api-service)
    - [Table of Contents](#table-of-contents)
    - [General Endpoint](#general-endpoint)
      - [Root URL](#root-url)
    - [Order Endpoints](#order-endpoints)
      - [List All Orders](#list-all-orders)
      - [Create a New Order](#create-a-new-order)
      - [Read an Order](#read-an-order)
      - [Update an Order](#update-an-order)
      - [Delete an Order](#delete-an-order)
    - [Item Endpoints](#item-endpoints)
      - [List All Items in an Order](#list-all-items-in-an-order)
      - [Create a New Item in an Order](#create-a-new-item-in-an-order)
      - [Read an Item from an Order](#read-an-item-from-an-order)
      - [Update an Item in an Order](#update-an-item-in-an-order)
      - [Delete an Item from an Order](#delete-an-item-from-an-order)
  - [Error Handling](#error-handling)
    - [CLI Commands](#cli-commands)
  - [Testing](#testing)
    - [Running Tests](#running-tests)
    - [Test Coverage](#test-coverage)
  - [Project Structure](#project-structure)
  - [Development Environment](#development-environment)
    - [VSCode Dev Containers](#vscode-dev-containers)
    - [Docker](#docker)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)

---

### General Endpoint

#### Root URL

- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns a JSON object containing information about the Order REST API Service, including available endpoints and their corresponding methods and URLs.
- **Response**:

    ```json
    {
        "name": "Order REST API Service",
        "version": "1.0",
        "description": "This is a RESTful service for managing orders. You can create, read, update, and delete orders, as well as manage items within orders.",
        "paths": {
            "list_orders": {
                "method": "GET",
                "url": "http://127.0.0.1:5000/orders"
            },
            ... other apis ...
            "get_item": {
                "method": "GET",
                "url": "http://127.0.0.1:5000/orders/{order_id}/items/{product_id}"
            },
        }
    }
    ```

- **Status Code**: `200 OK`

**Note**: The URLs in the response will reflect the actual host and port where your service is running. The `url_for` function in Flask generates these URLs dynamically.

---

### Order Endpoints

#### List All Orders

- **URL**: `/orders`
- **Method**: `GET`
- **Description**: Retrieves all orders sorted by date in descending order.
- **Response**:

    ```json
    [
        {
            "id": 2,
            "date": "2024-10-16",
            "status": 1,
            "amount": 49.98,
            "address": "456 Elm St",
            "customer_id": 42
        },
        {
            "id": 1,
            "date": "2024-10-15",
            "status": 2,
            "amount": 99.99,
            "address": "123 Main St",
            "customer_id": 24
        }
    ]
    ```

- **Status Code**: `200 OK`

---

#### Create a New Order

- **URL**: `/orders`
- **Method**: `POST`
- **Description**: Creates a new order with the provided details.
- **Request Headers**:

    - `Content-Type: application/json`

- **Request Body**:

    ```json
    {
        "id": 3,
        "date": "2024-10-17",
        "status": 1,
        "amount": 150.00,
        "address": "789 Oak Ave",
        "customer_id": 55
    }
    ```

- **Response**:

    ```json
    {
        "id": 3,
        "date": "2024-10-17",
        "status": 1,
        "amount": 150.00,
        "address": "789 Oak Ave",
        "customer_id": 55
    }
    ```

- **Status Code**: `201 Created`
- **Headers**:

    - `Location`: `http://127.0.0.1:5000/orders/3`

**Note**: In typical RESTful APIs, the `id` is generated by the server and should not be provided in the request body when creating a new resource. However, based on the provided code, the `id` is expected. Adjust your implementation accordingly.

---

#### Read an Order

- **URL**: `/orders/{order_id}`
- **Method**: `GET`
- **Description**: Retrieves details of a specific order by its ID.
- **Response**:

    ```json
    {
        "id": 1,
        "date": "2024-10-15",
        "status": 2,
        "amount": 99.99,
        "address": "123 Main St",
        "customer_id": 24
    }
    ```

- **Status Code**: `200 OK`

---

#### Update an Order

- **URL**: `/orders/{order_id}`
- **Method**: `PUT`
- **Description**: Updates an existing order with new information.
- **Request Headers**:

    - `Content-Type: application/json`

- **Request Body**:

    ```json
    {
        "id": 1,
        "date": "2024-10-15",
        "status": 3,
        "amount": 109.99,
        "address": "123 Main St, Apt 4",
        "customer_id": 24
    }
    ```

- **Response**:

    ```json
    {
        "id": 1,
        "date": "2024-10-15",
        "status": 3,
        "amount": 109.99,
        "address": "123 Main St, Apt 4",
        "customer_id": 24
    }
    ```

- **Status Code**: `200 OK`

---

#### Delete an Order

- **URL**: `/orders/{order_id}`
- **Method**: `DELETE`
- **Description**: Deletes an order by its ID.
- **Response**:

    - **Status Code**: `204 No Content`

---

### Item Endpoints

#### List All Items in an Order

- **URL**: `/orders/{order_id}/items`
- **Method**: `GET`
- **Description**: Retrieves all items associated with a specific order.
- **Response**:

    ```json
    [
        {
            "order_id": 1,
            "product_id": 101,
            "price": 19.99,
            "quantity": 2
        },
        {
            "order_id": 1,
            "product_id": 102,
            "price": 29.99,
            "quantity": 1
        }
    ]
    ```

- **Status Code**: `200 OK`

---

#### Create a New Item in an Order

- **URL**: `/orders/{order_id}/items`
- **Method**: `POST`
- **Description**: Adds a new item to an existing order.
- **Request Headers**:

    - `Content-Type: application/json`

- **Request Body**:

    ```json
    {
        "order_id": 1,
        "product_id": 103,
        "price": 9.99,
        "quantity": 3
    }
    ```

- **Response**:

    ```json
    {
        "order_id": 1,
        "product_id": 103,
        "price": 9.99,
        "quantity": 3
    }
    ```

- **Status Code**: `201 Created`
- **Headers**:

    - `Location`: `http://127.0.0.1:5000/orders/1/items`

**Note**: The `order_id` in the request body should match the `order_id` in the URL. In practice, you might not need to provide `order_id` in the request body since it's obtained from the URL.

---

#### Read an Item from an Order

- **URL**: `/orders/{order_id}/items/{product_id}`
- **Method**: `GET`
- **Description**: Retrieves details of a specific item within an order.
- **Response**:

    ```json
    {
        "order_id": 1,
        "product_id": 101,
        "price": 19.99,
        "quantity": 2
    }
    ```

- **Status Code**: `200 OK`

---

#### Update an Item in an Order

- **URL**: `/orders/{order_id}/items/{product_id}`
- **Method**: `PUT`
- **Description**: Updates details of a specific item within an order.
- **Request Headers**:

    - `Content-Type: application/json`

- **Request Body**:

    ```json
    {
        "order_id": 1,
        "product_id": 101,
        "price": 18.99,
        "quantity": 3
    }
    ```

- **Response**:

    ```json
    {
        "order_id": 1,
        "product_id": 101,
        "price": 18.99,
        "quantity": 3
    }
    ```

- **Status Code**: `200 OK`

---

#### Delete an Item from an Order

- **URL**: `/orders/{order_id}/items/{product_id}`
- **Method**: `DELETE`
- **Description**: Deletes a specific item from an order.
- **Response**:

    - **Status Code**: `204 No Content`

---

## Error Handling

The API returns standard HTTP status codes to indicate the success or failure of an API request. Possible status codes include:

- `200 OK`: The request was successful.
- `201 Created`: The resource was successfully created.
- `204 No Content`: The request was successful, but there is no content to return.
- `400 Bad Request`: The request was invalid or cannot be served.
- `404 Not Found`: The requested resource could not be found.
- `415 Unsupported Media Type`: The request's content type is invalid or not supported.
- `500 Internal Server Error`: An error occurred on the server.

Error responses typically include a JSON object with an `error` message:

```json
{
    "error": "Description of the error"
}
```

---




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

