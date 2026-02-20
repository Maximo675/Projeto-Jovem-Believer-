#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test simples para isolar problema de erro 426
"""
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/test')
def test():
    return jsonify({'message': 'teste ok'})

if __name__ == '__main__':
    print("Iniciando Flask simples na porta 5002...")
    app.run(host='127.0.0.1', port=5002, debug=False)
