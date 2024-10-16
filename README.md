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

### API Endpoints

Below is the updated **API Endpoints** section of the `README.md`, organized as per your specifications and including sample request and response examples based on your provided code.Z

#### General Endpoint
### API Endpoints

#### General Endpoint

- **Root URL**

    - **URL**: `/`

    - **Method**: `GET`

    - **Description**: Returns a JSON object containing information about the Order REST API Service, including available endpoints and their corresponding methods and URLs.

    - **Response**:

        ```json
        {
            "name": "Order REST API Service",
            "version": "1.0",
            "description": "This is a RESTful service for managing order.You can create, update, delete, read an order, and get all order.You can also create, update, delete, get an item and get all item in a given order.",
            "paths": {
                "list_orders": {
                    "method": "GET",
                    "url": "http://127.0.0.1:8080/orders"
                },
                ... other api endpoints ...
            }
        }
        ```

    - **Status Code**: `200 OK`

**Note**: The URLs in the response will reflect the actual host and port where your service is running. The `url_for` function in Flask generates these URLs dynamically.

---

#### Order Endpoints

- **List All Orders**

    - **URL**: `/orders`
    - **Method**: `GET`
    - **Description**: Retrieves all orders sorted by date in descending order.
    - **Response**:

      ```json
      [
          {
              "id": 2,
              "customer_name": "John Doe",
              "date_created": "2024-10-16T12:34:56",
              "date_updated": "2024-10-16T12:34:56",
              "status": "processing",
              "items": [
                  {
                      "product_id": 101,
                      "quantity": 2,
                      "price": 19.99
                  }
              ]
          },
          {
              "id": 1,
              "customer_name": "Jane Smith",
              "date_created": "2024-10-15T11:22:33",
              "date_updated": "2024-10-15T11:22:33",
              "status": "shipped",
              "items": [
                  {
                      "product_id": 102,
                      "quantity": 1,
                      "price": 49.99
                  }
              ]
          }
      ]
      ```

    - **Status Code**: `200 OK`

- **Create a New Order**

    - **URL**: `/orders`
    - **Method**: `POST`
    - **Description**: Creates a new order with the provided details.
    - **Request Body**:

      ```json
      {
          "customer_name": "Alice Johnson",
          "status": "processing",
          "items": [
              {
                  "product_id": 103,
                  "quantity": 1,
                  "price": 29.99
              },
              {
                  "product_id": 104,
                  "quantity": 2,
                  "price": 9.99
              }
          ]
      }
      ```

    - **Response**:

      ```json
      {
          "id": 3,
          "customer_name": "Alice Johnson",
          "date_created": "2024-10-16T13:00:00",
          "date_updated": "2024-10-16T13:00:00",
          "status": "processing",
          "items": [
              {
                  "product_id": 103,
                  "quantity": 1,
                  "price": 29.99
              },
              {
                  "product_id": 104,
                  "quantity": 2,
                  "price": 9.99
              }
          ]
      }
      ```

    - **Status Code**: `201 Created`

- **Read an Order**

    - **URL**: `/orders/{order_id}`
    - **Method**: `GET`
    - **Description**: Retrieves details of a specific order by its ID.
    - **Response**:

      ```json
      {
          "id": 1,
          "customer_name": "Jane Smith",
          "date_created": "2024-10-15T11:22:33",
          "date_updated": "2024-10-15T11:22:33",
          "status": "shipped",
          "items": [
              {
                  "product_id": 102,
                  "quantity": 1,
                  "price": 49.99
              }
          ]
      }
      ```

    - **Status Code**: `200 OK`

- **Update an Order**

    - **URL**: `/orders/{order_id}`
    - **Method**: `PUT`
    - **Description**: Updates an existing order with new information.
    - **Request Body**:

      ```json
      {
          "customer_name": "Jane Smith",
          "status": "delivered"
      }
      ```

    - **Response**:

      ```json
      {
          "id": 1,
          "customer_name": "Jane Smith",
          "date_created": "2024-10-15T11:22:33",
          "date_updated": "2024-10-16T14:00:00",
          "status": "delivered",
          "items": [
              {
                  "product_id": 102,
                  "quantity": 1,
                  "price": 49.99
              }
          ]
      }
      ```

    - **Status Code**: `200 OK`

- **Delete an Order**

    - **URL**: `/orders/{order_id}`
    - **Method**: `DELETE`
    - **Description**: Deletes an order by its ID.
    - **Response**:

      - **Status Code**: `204 No Content`

---

#### Item Endpoints

- **List All Items in an Order**

    - **URL**: `/orders/{order_id}/items`
    - **Method**: `GET`
    - **Description**: Retrieves all items associated with a specific order.
    - **Response**:

      ```json
      [
          {
              "product_id": 103,
              "quantity": 1,
              "price": 29.99
          },
          {
              "product_id": 104,
              "quantity": 2,
              "price": 9.99
          }
      ]
      ```

    - **Status Code**: `200 OK`

- **Create a New Item in an Order**

    - **URL**: `/orders/{order_id}/items`
    - **Method**: `POST`
    - **Description**: Adds a new item to an existing order.
    - **Request Body**:

      ```json
      {
          "product_id": 105,
          "quantity": 1,
          "price": 19.99
      }
      ```

    - **Response**:

      ```json
      {
          "order_id": 3,
          "product_id": 105,
          "quantity": 1,
          "price": 19.99
      }
      ```

    - **Status Code**: `201 Created`

- **Read an Item from an Order**

    - **URL**: `/orders/{order_id}/items/{product_id}`
    - **Method**: `GET`
    - **Description**: Retrieves details of a specific item within an order.
    - **Response**:

      ```json
      {
          "order_id": 3,
          "product_id": 103,
          "quantity": 1,
          "price": 29.99
      }
      ```

    - **Status Code**: `200 OK`

- **Update an Item in an Order**

    - **URL**: `/orders/{order_id}/items/{product_id}`
    - **Method**: `PUT`
    - **Description**: Updates details of a specific item within an order.
    - **Request Body**:

      ```json
      {
          "quantity": 2,
          "price": 28.99
      }
      ```

    - **Response**:

      ```json
      {
          "order_id": 3,
          "product_id": 103,
          "quantity": 2,
          "price": 28.99
      }
      ```

    - **Status Code**: `200 OK`

- **Delete an Item from an Order**

    - **URL**: `/orders/{order_id}/items/{product_id}`
    - **Method**: `DELETE`
    - **Description**: Deletes a specific item from an order.
    - **Response**:

      - **Status Code**: `204 No Content`

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

