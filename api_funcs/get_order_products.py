# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import uuid
import sqlite3
from sqlite3 import Error as Err
import ast


def get_order_products(order_id):
    try:
        con = sqlite3.connect('shop.db')
        cur = con.cursor()
        sql = "SELECT products FROM orders WHERE order_id = ?"
        data = (order_id,)
        cur.execute(sql, data)

        products = cur.fetchall()[0][0]
        con.close()

        # Convert str to list
        products = ast.literal_eval(str(products))
    except:
        return "Not found", 404

    return products, 201