import time
import requests
import threading
import logging
from formula_1_iot_utils import CommunicationInterface
from flask import Flask, jsonify, Response

pit_stop = Flask(__name__)

@pit_stop.route('/')
def pit_stop_interface():
    while True:
        try:
            res = requests.get('http://formula_1_car:5000')
            pit_stop.logger.info(f"[Pit Stop] Got from Formula 1 Car: {res.text}")
        except Exception as e:
            pit_stop.logger.error(f"[Pit Stop] Error: {e}")
        return 

if __name__ == '__main__':
    threading.Thread(target=pit_stop_interface, daemon=True).start()
    pit_stop.run(host='0.0.0.0', port=5000, debug=True)
