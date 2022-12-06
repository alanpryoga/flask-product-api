# Flask Product API
## Prerequisites
* Docker

## Setup
If already installed Docker on local machine, type this command on 
Terminal ``docker compose up`` to build and run dependencies container 
(postgres, redis) and app container.

Then visit ``localhost:8080``, make sure ``Hello world!`` message
appear on the screen.

## Architecture
This app consist of three layers: ``view``, ``service``, and ``repository`` 
* ``view``, the presentation layer. Get and validate requests and response 
as JSON data.
* ``service``, the business layer. Perform business logic by getting input from 
view, invoke data access layer, and return the output.
* ``repository``, the data access layer. Perform data access to specific 
storage engine or databases.

Each layer will be injected and follow inversion of control. I choose this 
architecture to easier separate the concerns. And easy to replace the implementation
of each layer. For example, if we want to replace from ``REST`` to ``gRPC``
just replace the implementation of ``view`` layer to ``gRPC``, and vice versa for
``repository`` layer.

## Usage
### Add Product
``POST http://localhost:8080/products``

#### Request (JSON Payload)
```json
{
  "name": "Product name",
  "price": 50000,
  "description": "Product description",
  "quantity": 100
}
```
| Field    | Validation           |
|----------|----------------------|
| name     | mandatory            |
| price    | mandatory and number |
| quantity | mandatory and number |

#### Response
200 OK
```json
{
  "status": "ok",
  "message": "Successfully create new product."
}
```

400 Bad Request
```json
{
  "status": "error",
  "message": "Fields validation failed.",
  "errors": [
    {
      "name": "field name is mandatory."
    }
  ]
}
```

500 Internal Server Error
```json
{
  "status": "error",
  "message": "Internal server error."
}
```

### List of Products
``GET http://localhost:8080/products``

#### Sorting
| URL                                                            | Description                |
|----------------------------------------------------------------|----------------------------|
| ``http://localhost:8080/products?sort_by=id&sort_dir=asc``     | Sorting by oldest          |
| ``http://localhost:8080/products?sort_by=id&sort_dir=desc``    | Sorting by newest          |
| ``http://localhost:8080/products?sort_by=name&sort_dir=asc``   | Sorting by name (A-Z)      |
| ``http://localhost:8080/products?sort_by=name&sort_dir=desc``  | Sorting by name (Z-A)      |
| ``http://localhost:8080/products?sort_by=price&sort_dir=asc``  | Sorting by cheapest first  |
| ``http://localhost:8080/products?sort_by=price&sort_dir=desc`` | Sorting by expensive first |

By default, if not sorting parameters are included. 
It will sort by ``id`` and sort direction to ``desc``

#### Response
200 OK
```json
{
    "status": "ok",
    "message": "Successfully fetch products.",
    "data": [
        {
            "id": 3,
            "quantity": 2,
            "price": 20000,
            "name": "Product 3",
            "description": "Desc of Product 3"
        },
        {
            "id": 2,
            "quantity": 10,
            "price": 50000,
            "name": "Product 2",
            "description": "Desc of Product 2"
        },
        {
            "id": 1,
            "quantity": 100,
            "price": 100000,
            "name": "Product 1",
            "description": "Desc of Product 1"
        }
    ]
}
```