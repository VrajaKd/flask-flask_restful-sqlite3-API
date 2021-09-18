# -*- coding: utf-8 -*-
from flask import request
import sqlite3
import ast

from all_products import products

def update_order_in_db(current_products, order_id, total):
    # Update order in db
    con = sqlite3.connect('shop.db')
    cur = con.cursor()
    sql = "UPDATE orders SET products = ?, total = ? WHERE order_id = ?"
    data = (str(current_products), str(total), order_id,)
    cur.execute(sql, data)
    con.commit()

def add_replacement_product(order_id, product_id):
    order_exists = False
    product_exists = False
    try:
        new_product_id = request.get_json()['replaced_with']['product_id']
        new_quantity = request.get_json()['replaced_with']['quantity']
    except:
        return 'Input not correct', 400

    if new_product_id and new_quantity:
        con = sqlite3.connect('shop.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM orders")
        orders = cur.fetchall()

        # Check if order exists in the DB
        for order in orders:
            if order[4] == order_id:
                order_exists = True

                current_products = order[5]
                # Convert product str to list
                current_products = ast.literal_eval(str(current_products))

                c = 0
                product_exists = False
                # Pick correct product from order products
                for current_product in current_products:
                    if current_product['id'] == product_id:
                        new_name = ''
                        new_price = ''
                        products_list = products()

                        for product in products_list:
                            if product['id'] == new_product_id:
                                new_name = product['name']
                                new_price = product['price']

                        current_products[c]['name'] = new_name
                        current_products[c]['price'] = new_price
                        current_products[c]['replaced_with'] = current_product['product_id']
                        current_products[c]['product_id'] = new_product_id
                        current_products[c]['quantity'] = new_quantity

                        product_exists = True
                    c += 1

                # Update total price
                total = 0
                for current_product in current_products:
                    total = float(current_product['price']) * float(current_product['quantity']) + total
                    total = round(total, 2)

                update_order_in_db(current_products, order_id, total)

    if not order_exists:
        return 'Order not found', 404
    if not product_exists:
        return 'Product not found', 404
    return 'OK', 201
