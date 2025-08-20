from __future__ import annotations

import threading
import time

import requests
from flask import Flask
from formula_1_iot_utils import Formula1CarDataEvaluation, MessagesDisplay

pit_stop = Flask(__name__)
@pit_stop.route('/')
def pit_stop_interface():
    while True:
        time.sleep(1)
        try:
            with pit_stop.app_context():
                res = requests.get('http://formula_1_car:5000', timeout=5)
                data = res.json()
                formula_1_car_params = MessagesDisplay().display_formula_1_cars_data(data)
                pit_stop.logger.info(f"[Pit Stop] Got from Formula 1 Car: {formula_1_car_params}")

                evaluation = Formula1CarDataEvaluation(data["id"])
                return evaluation.convert_condition_report_to_message(data)

        except Exception as e:
            pit_stop.logger.error(f"[Pit Stop] Error: {e}")

if __name__ == '__main__':
    threading.Thread(target=pit_stop_interface, daemon=True).start()
    pit_stop.run(host='0.0.0.0', port=5000, debug=True)
