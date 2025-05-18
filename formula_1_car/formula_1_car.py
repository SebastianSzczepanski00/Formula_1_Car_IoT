import threading
import time
from formula_1_iot_utils import CommunicationInterface, Formula1Car
import requests
from flask import Flask, Response

formula_1_car = Flask(__name__)


@formula_1_car.route('/')
def send_data():
    """Send data to the Pit Stop."""
    def generate():
        while True:
            message = Formula1Car(id=1).convert_data_to_message()
            yield CommunicationInterface().send_message(message)
            time.sleep(2)
    return Response(generate(), mimetype='text/event-stream')

def formula_1_car_interface():
    while True:
        try:
            res = requests.get('http://pit_stop:5000')
            formula_1_car.logger.info(f"[Formula 1 Car] Got from Pit Stop: {res.text}")

        except Exception as e:
            formula_1_car.logger.error(f"[Formula 1 Car] Error: {e}")
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=formula_1_car_interface, daemon=True).start()
    formula_1_car.run(host='0.0.0.0', port=5000, debug=True)