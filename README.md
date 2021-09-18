A lightweight example of an e-store API with Flask, SQLite and Flask-RESTful.

## How to set up ##

- Install Flask-RESTful with pip
    ```
    pip install flask-restful
    ```

- Install the packages
    ```
    pip install -r requirements.txt
    ```
    
- Run Flask 
    ```
    python api.py
    ```


#### Working queries: ####

* GET /api/products - list of all available products
    ```
    curl https://homework.solutional.ee/api/products
    ```

* POST /api/orders - create new order
    ```
    curl -X POST https://homework.solutional.ee/api/orders
    ```

* GET /api/orders/:order_id - get order details
    ```
    curl https://homework.solutional.ee/api/orders/:order_id
    ```

* PATCH /api/orders/:order_id - update order
    ```
    curl -X PATCH --data '{"status": "PAID"}' -H "Content-Type: application/json" \
      https://homework.solutional.ee/api/orders/:order_id
    ```

* GET /api/orders/:order_id/products - get order products
    ```
    curl https://homework.solutional.ee/api/orders/:order_id/products
    ```

* POST /api/orders/:order_id/products - add products to order
    ```
    curl --data '[123]' -H "Content-Type: application/json" \
      https://homework.solutional.ee/api/orders/:order_id/products
    ```

* PATCH /api/orders/:order_id/products/:product_id - update product quantity
    ```
    curl -X PATCH --data '{"quantity": 33}' -H "Content-Type: application/json" \
      https://homework.solutional.ee/api/orders/:order_id/products/:product_id
    ```

* PATCH /api/orders/:order_id/products/:product_id - add a replacement product
    ```
    curl -X PATCH --data '{"replaced_with": {"product_id": 123, "quantity": 6}}' -H "Content-Type: application/json" \
      https://homework.solutional.ee/api/orders/:order_id/products/:product_id
    ```
