# -*- coding: utf-8 -*-
import uuid
import sqlite3
from sqlite3 import Error as Err


def create_new_order():
    order_id = str(uuid.uuid4())
    order = {'amount': {'discount': '0.00', 'paid': '0.00', 'returns': '0.00', 'total': '0.00'}, 'id': order_id,
             'products': [], 'status': 'NEW'}

    # Save order to db
    # try:
    con = sqlite3.connect('shop.db')
    cur = con.cursor()
    sql = "INSERT INTO orders(discount, paid, returns, total, order_id, products, status) VALUES (?,?,?,?,?,?,?)"
    data = ('0.00', '0.00', '0.00', '0.00', order_id, '[]', 'NEW',)
    cur.execute(sql, data)
    con.commit()
    con.close()
    # except Err:
    #     return "DB error", 404

    return order, 201
