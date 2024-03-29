# -*- coding: utf-8 -*-
from flask import request, send_from_directory                                                                                                 
from flask import Flask                                                                                                                                
from flask import Response                                                                                                                             
import flask                                                                                                                                           
import json                                                                                                                                            
import logging                                                                                                                                         
import sys                                                                                                                                             
import os                                                                                                                                              
from MyQR import myqr                                                                                                                                                   
import random  

app = Flask(__name__)                                                                                                                                   
app.debug = True                                                                                                                         

ppfun_url = "https://ppfun.fun/"
assets_dir = app.root_path + "/assets/"
output_dir = app.root_path + "/static/"

def INVALID_PARAM():
    e = {"error":"非法输入"}
    return make_response(400, e)

def LOGIN_FAIL():
    e = {"error":"登陆失败"}
    return make_response(400, e)

def  FORBIDDEN():
    e = {"error":"forbidden"}
    return make_response(403, e)


def make_response(status_code, data = None):
    if data:
        res = flask.make_response(json.dumps(data), status_code)
        res.headers['Content-Type'] = "application/json"
    else:
        res = flask.make_response("", status_code)

    return res


@app.route("/qrcode/<type>/<image_name>", methods=["GET"])
def getQrcode(type, image_name):
    if not type or not image_name:
        return INVALID_PARAM()

    sava_directory = str(output_dir + type)
    save_name = str(image_name)

    if not os.path.exists(sava_directory):
        os.makedirs(sava_directory)

    if not os.path.exists(sava_directory + '/' + save_name):
        words = str(ppfun_url + type + "?" + "hash=" + image_name[:-4])
        imagelist = os.listdir(assets_dir)
        picture = str(assets_dir + random.sample(imagelist, 1)[0])
        version, level, qr_name = myqr.run(
            words=words,
            version=1,
            level='H',
            picture=picture,
            colorized=True,
            contrast=1.0,
            brightness=1.0,
            save_name=save_name,
            save_dir=sava_directory
        )

    return send_from_directory(output_dir + type + "/", image_name, mimetype='image/vnd.microsoft.icon')


def init_logger(logger):
    root = logger
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(filename)s:%(lineno)d -  %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)    

log = logging.getLogger('')
init_logger(log)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8011)
