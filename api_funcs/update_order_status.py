# -*- coding: utf-8 -*-
from flask import request
import sqlite3


def update_order_status(order_id):

    try:
        status = request.get_json()['status']
    except:
        return 'Status not correct', 400

    #  Check if order exists
    o_id = ''
    try:
        con = sqlite3.connect('shop.db')
        cur = con.cursor()
        sql = "SELECT order_id FROM orders WHERE order_id = ?"
        data = (order_id,)
        cur.execute(sql, data)

        try:
            o_id = cur.fetchall()[0][0]
        except: pass

        if not o_id:
            return "Order not found", 400
    except:
        return "DB error", 400

    if o_id and status:
        try:
            # Update order in db
            con = sqlite3.connect('shop.db')
            cur = con.cursor()
            sql = "UPDATE orders SET status = ? WHERE order_id = ?"
            data = (status, order_id,)
            cur.execute(sql, data)
            con.commit()

            return "OK", 201
        except:
            return "DB error", 400