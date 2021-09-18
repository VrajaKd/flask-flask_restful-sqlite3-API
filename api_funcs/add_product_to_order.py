# -*- coding: utf-8 -*-
from flask import Flask, request
import uuid
import sqlite3
import ast


def update_order_in_db(current_products, order_id, total):
    # Update order in db
    con = sqlite3.connect('shop.db')
    cur = con.cursor()
    sql = "UPDATE orders SET products = ?, total = ? WHERE order_id = ?"
    data = (str(current_products), str(total), order_id,)
    cur.execute(sql, data)
    con.commit()


def add_product_to_order(order_id, products):
    order_exists = False
    product_exists = False
    product_code = ''
    try:
        product_code = (request.get_json())[0]
    except:
        pass

    con = sqlite3.connect('shop.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()

    # Check if order exists in the DB
    for order in orders:
        if order[4] == order_id:
            order_exists = True

            # Check if product exists in stock list
            for product in products:
                if product['id'] == product_code:
                    product_exists = True

                    # Check is there already any products in order
                    current_products = order[5]

                    # Create new product id
                    new_product_id = str(uuid.uuid4())

                    # Add product to order
                    if current_products:
                        # Convert str to list
                        current_products = ast.literal_eval(str(current_products))
                        # Check if product already exists
                        exists = False

                        # If current products exists and added product exists, update order
                        c = 0
                        for current_product in current_products:
                            if str(current_product['product_id']) == str(product_code):
                                current_products[c]['quantity'] = current_products[c]['quantity'] + 1
                                exists = True

                                # Update total price
                                total = 0
                                for current_product in current_products:
                                    total = (float(current_product['price']) * float(current_product['quantity'])) + total
                                    total = round(total, 2)

                                update_order_in_db(current_products, order_id, total)
                            c += 1

                        # If current products exists and added product do not exists, update order
                        if not exists:
                            new_product = {'id': new_product_id, 'name': product['name'], 'price': str(product['price']),
                                           'product_id': str(product['id']), 'quantity': 1, 'replaced_with': None}
                            current_products.append(new_product)

                            # Update total price
                            total = 0
                            for current_product in current_products:
                                total = (float(current_product['price']) * float(current_product['quantity'])) + total
                                total = round(total, 2)

                            update_order_in_db(current_products, order_id, total)

                    if not current_products:
                        total = float(product['price'])
                        total = round(total, 2)
                        new_product = "[{'id': '" + new_product_id + "', 'name': '" + product[
                            'name'] + "' , 'price': '" + str(product['price']) + "', 'product_id': " + str(
                            product['id']) + ", 'quantity': 1, 'replaced_with': None}]"

                        update_order_in_db(new_product, order_id, total)

    if not order_exists:
        return 'Order not found', 404
    if not product_exists:
        return 'Product not found', 404
    return 'OK', 201
