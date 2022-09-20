from flask import Flask, render_template
import requests
import json
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    pool_data = get_pool_data()
    worker_data = get_worker_data()
    return render_template("index.html", worker_data=worker_data, pool_data=pool_data)

def get_pool_data():
    pool_url = f"https://kano.is/index.php?k=api&username=cmb-bitcoin&api={API_KEY}&json=y"
    pool_data = ((requests.request("GET", pool_url))).json()
    return(pool_data)

def get_worker_data():
    worker_url = f"https://kano.is/index.php?k=api&username=cmb-bitcoin&api={API_KEY}&json=y&work=y"
    worker_data = ((requests.request("GET", worker_url))).json()
    return(worker_data)

app.run(host="0.0.0.0", port=80)