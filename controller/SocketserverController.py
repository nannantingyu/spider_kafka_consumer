# -*- coding: utf-8 -*-
from Controller import Controller
import json, re, requests, logging
import socketio
import eventlet
from flask import Flask, render_template

sio = socketio.Server()
app = Flask(__name__)

@app.route('/')
def index():
    """Serve the client-side application."""
    return render_template('index.html')

@sio.on('connect')
def connect(sid, environ):
    sio.emit("aaa_response", "hello, aaa_response")
    print('connect ', sid)

@sio.on('kuaixun')
def message(sid, data):
    print('kuaixun ', data)
    sio.emit("kx", json.loads(data))

@sio.on('crawl_jin10_kuaixun')
def message(sid, data):
    print('crawl_jin10_kuaixun ', data)
    sio.emit("crawl_jin10_kuaixun", json.loads(data))

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='logs/article.log',
                filemode='w')

class SocketserverController(Controller):
    def __init__(self, topic=""):
        super(SocketserverController, self).__init__(topic)

    def run(self):
        global app
        app = socketio.Middleware(sio, app)
        eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 8002)), app)
