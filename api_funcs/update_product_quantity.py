# -*- coding: utf-8 -*-
from flask import request
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

def update_product_quantity(order_id, product_id):
    order_exists = False
    product_exists = False
    try:
        quantity = request.get_json()['quantity']
        print(request.get_json())
    except:
        return 'Quantity not correct', 400

    if quantity:
        con = sqlite3.connect('shop.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM orders")
        orders = cur.fetchall()

        # Check if order exists in the DB
        for order in orders:
            if order[4] == order_id:
                order_exists = True

                current_products = order[5]
                # Convert str to list
                current_products = ast.literal_eval(str(current_products))

                c = 0
                product_exists = False
                for current_product in current_products:
                    if current_product['id'] == product_id:
                        current_products[c]['quantity'] = quantity
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
