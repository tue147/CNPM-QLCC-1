from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from mysql.connector import Error, InterfaceError
from backend import *
import backend


def catching_error(func):
    def handling():
        try:
            func()
        except InterfaceError as e:
            backend.mydb = connect_db()
            # response = jsonify({"error": "Lỗi mất kết nối với CSDL!"})
            # response.status_code = 404 
            # return response
            return render_template('error.html', error_code= "Lỗi mất kết nối với CSDL!")
        except Error as e:
            return render_template('error.html', error_code=e.msg)

