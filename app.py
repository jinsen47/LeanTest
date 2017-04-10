# coding: utf-8
import json
from datetime import datetime

import leancloud
import requests
from flask import Flask, request, Response
from flask import render_template
from flask_sockets import Sockets

from views.todos import todos_view

app = Flask(__name__)
sockets = Sockets(app)

# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/time')
def time():
    return str(datetime.now())


@app.route('/gank/<category>/<page>')
def gank(category, page):
    url = 'http://gank.io/api/search/query/listview/category/%s/count/5/page/%s' % (category, page)
    requestAPI = requests.get(url)
    return Response(json.dumps(requestAPI.json()), mimetype='application/json')


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)
