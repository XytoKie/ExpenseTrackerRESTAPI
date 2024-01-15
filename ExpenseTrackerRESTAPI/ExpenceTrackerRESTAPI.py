from flask import Flask, jsonify, request

app = Flask(__name__)

users = {}
categories = {}
records = {}


if __name__ == '__main__':
    app.run(debug=True)
