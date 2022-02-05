from flask import Flask
from flask import request
from flask import render_template
from flask import url_for, redirect, flash
from flask import abort
from flask import session
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from datetime import datetime
from datetime import timedelta
from werkzeug.utils import secure_filename
import time
import math
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/flow" 
app.config['SECRET_KEY'] = 'password1'

import os

BOARD_IMAGE_PATH = "C:/Users/cgkim449/study/images"
BOARD_ATTACH_FILE_PATH = "C:/Users/cgkim449/study/uploads"

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['BOARD_IMAGE_PATH'] = BOARD_IMAGE_PATH
app.config['BOARD_ATTACH_FILE_PATH'] = BOARD_ATTACH_FILE_PATH
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024

if not os.path.exists(app.config["BOARD_IMAGE_PATH"]):
    os.mkdir(app.config["BOARD_IMAGE_PATH"])
if not os.path.exists(app.config["BOARD_ATTACH_FILE_PATH"]):
    os.mkdir(app.config["BOARD_ATTACH_FILE_PATH"])

mongo = PyMongo(app)

from .common import login_required, rand_generator, allowed_file, check_filename, hash_password, check_password
from .filter import format_datetime
from . import board
from . import member

app.register_blueprint(board.blueprint)
app.register_blueprint(member.blueprint)
