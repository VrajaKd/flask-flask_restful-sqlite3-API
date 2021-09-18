# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import reqparse, Api, Resource
import sqlite3
import logging
import sys

from all_products import products
from api_funcs.create_new_order import create_new_order
from api_funcs.add_product_to_order import add_product_to_order
from api_funcs.get_order_products import get_order_products
from api_funcs.update_product_quantity import update_product_quantity
from api_funcs.get_order_details import get_order_details
from api_funcs.update_order_status import update_order_status
from api_funcs.add_replacement_product import add_replacement_product

app = Flask(__name__)
api = Api(app)

# Configure Logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

parser = reqparse.RequestParser()

con = sqlite3.connect('shop.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS orders
                   (discount text, paid text, returns text, total text, order_id text, products text, status text)''')
con.close()


# Get list of all available products
class ProductList(Resource):
    def get(self):
        return products()


# Create new order
class CreateNewOrder(Resource):
    def post(self):
        return create_new_order()


# Add product to order
class AddProductToOrder(Resource):
    def post(self, order_id):
        return add_product_to_order(order_id, products())


# Get order products
class GetOrderProducts(Resource):
    def get(self, order_id):
        return get_order_products(order_id)


# Update product quantity or Update order
class UpdateProductQuantityOrUpdateOrder(Resource):
    def patch(self, order_id, product_id):
        # Update product quantity
        try:
            if request.get_json()['quantity']:
                return update_product_quantity(order_id, product_id)
        except: pass

        # Update product
        try:
            if request.get_json()['replaced_with']:
                return add_replacement_product(order_id, product_id)
        except: pass


# Update product quantity
class GetOrderDetails(Resource):
    def get(self, order_id):
        return get_order_details(order_id)


# Update order
class UpdateOrderStatus(Resource):
    def patch(self, order_id):
        return update_order_status(order_id)


# Api resource routing
api.add_resource(ProductList, '/api/products')
api.add_resource(CreateNewOrder, '/api/orders')
api.add_resource(AddProductToOrder, '/api/orders/<order_id>/products')
api.add_resource(GetOrderProducts, '/api/orders/<order_id>/products')
api.add_resource(UpdateProductQuantityOrUpdateOrder, '/api/orders/<order_id>/products/<product_id>')
api.add_resource(GetOrderDetails, '/api/orders/<order_id>')
api.add_resource(UpdateOrderStatus, '/api/orders/<order_id>')


if __name__ == '__main__':
    app.run(debug=True)
