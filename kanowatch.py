from multiprocessing import pool
from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

KANO_API_KEY = os.getenv("KANO_API_KEY")
IFTTT_API_KEY = os.getenv("IFTTT_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    pool_data = get_pool_data()
    worker_data = get_worker_data()
    
    # if Kano found the latest block
    if int(pool_data.get('lastblockheight')) == int(pool_data.get('lastheight')):
        trigger_pool_alert()

    # if hashrate less than 50TH/s
    if(float(worker_data.get('w_hashrate5m:0')) < 50202206628511.703125):
        trigger_worker_alert()
    
    curr_time = datetime.datetime.now()
    # don't really want / need a front end right now but whatever
    return render_template("index.html",curr_time=curr_time, worker_data=worker_data, pool_data=pool_data)

def get_pool_data():
    pool_url = f"https://kano.is/index.php?k=api&username=cmb-bitcoin&api={KANO_API_KEY}&json=y"
    pool_data = ((requests.request("GET", pool_url))).json()
    return(pool_data)

def get_worker_data():
    worker_url = f"https://kano.is/index.php?k=api&username=cmb-bitcoin&api={KANO_API_KEY}&json=y&work=y"
    worker_data = ((requests.request("GET", worker_url))).json()
    return(worker_data)

def get_network_info():
    network_hashrate = (requests.get("https://blockchain.info/q/hashrate")).json()
    return network_hashrate

def trigger_pool_alert():
    event = "kano_found_a_block"
    requests.get(f"https://maker.ifttt.com/trigger/{event}/with/key/{IFTTT_API_KEY}")
    return 

def trigger_worker_alert():
    event = "worker_hashrate"
    requests.get(f"https://maker.ifttt.com/trigger/{event}/with/key/{IFTTT_API_KEY}")
    return 

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.getenv('PORT'))