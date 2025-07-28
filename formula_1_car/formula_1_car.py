from __future__ import annotations
import random
import threading
import time
from formula_1_iot_utils import CommunicationInterface, Formula1CarData
import requests
from flask import Flask, Response, jsonify

formula_1_car = Flask(__name__)


@formula_1_car.route('/')
def send_data():
    """Send data to the Pit Stop."""

    # Define the ranges for tire pressure, velocity, and engine temperature
    max_pressure = 40.0
    min_pressure = 0.0
    max_velocity = 350.0
    min_velocity = 0.0
    max_engine_temperature = 60.0
    min_engine_temperature = -40.0

    # Generate random data for the Formula 1 Car
    formula_1_car_data = Formula1CarData(id=1)
    formula_1_car_data.set_velocity(random.uniform(min_velocity, max_velocity))
    formula_1_car_data.set_tires_pressure(front_right=random.uniform(min_pressure, max_pressure),
                                          front_left=random.uniform(min_pressure, max_pressure),
                                          rear_right=random.uniform(min_pressure, max_pressure),
                                          rear_left=random.uniform(min_pressure, max_pressure))
    formula_1_car_data.set_engine_temperature(random.uniform(min_engine_temperature,
                                                             max_engine_temperature))

    # Send the data to the Pit Stop as JSON
    return formula_1_car_data.convert_data_to_message()

def formula_1_car_interface():
    while True:
        try:
            res = requests.get('http://pit_stop:5000')
            data = res.json()
            formula_1_car.logger.info(f"[Formula 1 Car] Got from Pit Stop: {data}")

        except Exception as e:
            formula_1_car.logger.error(f"[Formula 1 Car] Error: {e}")
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=formula_1_car_interface, daemon=True).start()
    formula_1_car.run(host='0.0.0.0', port=5000, debug=True)
