# -*- coding: utf-8 -*-
import sqlite3
import ast


def get_order_details(order_id):
    order_json = {}
    amount = {}
    try:
        con = sqlite3.connect('shop.db')
        cur = con.cursor()
        sql = "SELECT * FROM orders WHERE order_id = ?"
        data = (order_id,)
        cur.execute(sql, data)

        order_details = cur.fetchall()[0]
        con.close()


        # Convert str to list
        order_details = ast.literal_eval(str(order_details))

        amount['discount'] = order_details[0]
        amount['paid'] = order_details[1]
        amount['returns'] = order_details[2]
        amount['total'] = order_details[3]

        order_json['amount'] = amount
        order_json['id'] = order_details[4]

        order_json['products'] = ast.literal_eval(str(order_details[5]))
        order_json['status'] = order_details[6]

        return order_json, 201
    except:
        return "Not found", 404