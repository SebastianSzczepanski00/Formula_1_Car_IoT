from __future__ import annotations

import threading
import time
from random import uniform

import requests
import yaml
from flask import Flask
from formula_1_iot_utils import Formula1CarData, MessagesDisplay

formula_1_car = Flask(__name__)


@formula_1_car.route('/')
def send_data():
    """Send data to the Pit Stop."""

    time.sleep(1)
    # Define the ranges for tire pressure, velocity, and engine temperature
    file = open('/constants.yaml', 'r')
    constants = yaml.safe_load(file)
    max_engine_temperature = constants[0]["engine_temp_limits"]["absolute_max"]
    min_engine_temperature = constants[0]["engine_temp_limits"]["absolute_min"]
    max_pressure = constants[1]["tires_pressure_limits"]["absolute_max"]
    min_pressure = constants[1]["tires_pressure_limits"]["absolute_min"]
    max_velocity = constants[2]["velocity_limits"]["absolute_max"]
    min_velocity = constants[2]["velocity_limits"]["absolute_min"]

    # Generate random data for the Formula 1 Car
    formula_1_car_data = Formula1CarData(id=1)
    formula_1_car_data.set_velocity(uniform(min_velocity, max_velocity))
    formula_1_car_data.set_tires_pressure(front_right=uniform(min_pressure, max_pressure),
                                          front_left=uniform(min_pressure, max_pressure),
                                          rear_right=uniform(min_pressure, max_pressure),
                                          rear_left=uniform(min_pressure, max_pressure))
    formula_1_car_data.set_engine_temperature(uniform(min_engine_temperature,
                                                      max_engine_temperature))

    # Send the data to the Pit Stop as JSON
    return formula_1_car_data.convert_data_to_message()

def formula_1_car_interface():
    while True:
        time.sleep(1)
        try:
            with formula_1_car.app_context():
                res = requests.get('http://pit_stop:5000', timeout=5)
                data = res.json()
                formula_1_car_condition = MessagesDisplay().display_formula_1_cars_condition(data)
                formula_1_car.logger.info(f"[Formula 1 Car] Got from Pit Stop: {formula_1_car_condition}")

        except Exception as e:
            formula_1_car.logger.error(f"[Formula 1 Car] Error: {e}")

if __name__ == '__main__':
    threading.Thread(target=formula_1_car_interface, daemon=True).start()
    formula_1_car.run(host='0.0.0.0', port=5000, debug=True)
