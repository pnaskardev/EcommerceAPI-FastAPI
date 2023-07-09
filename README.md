
# E-Commerce FastAPI

The E-commerce API project is built using FastAPI, a modern and efficient Python framework for building web APIs. The project aims to provide a robust and scalable API for an e-commerce platform. It incorporates various features and functionalities essential for an e-commerce system, such as product management, order management, user authentication, and more.

## Features

- **Product Management**: The API allows CRUD (Create, Read, Update, Delete) operations for managing products. It includes endpoints for creating new products, retrieving product details, updating product information, and deleting products.

- **Order Management**: The API provides endpoints for creating and managing orders. Users can place orders by specifying the desired products and quantities. The API handles checking product availability, calculating order total amounts, and updating product quantities after successful orders.

- **Pagination**: The API includes pagination support for listing products and orders. It allows retrieving a limited number of records at a time and provides options for specifying the number of records and the starting point.

- **Database Integration**: The API interacts with a database, such as MongoDB, for storing and retrieving product and order information. It utilizes asynchronous database operations to improve performance and scalability.

- **Swagger Documentation**: FastAPI generates interactive API documentation using Swagger UI. It provides detailed information about available endpoints, request/response models, and allows users to interact with the API directly from the documentation.
## Run Locally

Clone the project

```bash
  git clone https://github.com/pnaskardev/EcommerceAPI-FastAPI
```

Go to the project directory

```bash
  cd EcommerceAPI-FastAPI
```

Create a python virtual environement

```bash
  python -m venv venv
```

Start the virtual environement

```bash
  venv\Scripts\activate
```

install required packages

```bash
  pip install -r requirements.txt
```

Start the Server

```bash
  uvicorn main:app --reload
```

Access the API at 

```bash
  http://127.0.0.1:8000/docs
```


## API Reference


#### List all the Products

```http
  GET /get-products/
```

#### Register to the platform

```http
  POST /post-products/
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name` | `string` | **Required** name of the product.  |
| `price` | `string` | **Required** price of the product |
| `quantity` | `string` | **Required**. quantity of the product |


#### Edit the product

```http
  PUT /edit-products/{product_id}
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `quantity` | `integer` | **Required**. quantity of the product |

#### List all the Orders

```http
  GET /get-orders/
```

#### Get a single Order

```http
   GET /orders/{order_id}
```

#### Post an Order 

```http
  POST /post-orders/
```
##### Scheme of Order
```
{
  "timestamp": "2023-07-09T00:08:37.563897",
  "items": [
    {
      "product_id": "string",
      "bought_quantity": 0
    }
  ],
  "user_address": {
    "city": "string",
    "country": "string",
    "zip_code": "string"
  }
}
```
## Authors

- [@pnaskardev](https://www.github.com/pnaskardev)

