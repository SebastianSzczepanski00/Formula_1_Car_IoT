import time
import requests
import threading
from formula_1_iot_utils import Formula1CarDataEvaluation
from flask import Flask

pit_stop = Flask(__name__)

@pit_stop.route('/')
def pit_stop_interface():
    while True:
        try:
            res = requests.get('http://formula_1_car:5000')
            data = res.json()
            pit_stop.logger.info(f"[Pit Stop] Got from Formula 1 Car: {data}")

            evaluation = Formula1CarDataEvaluation(data["id"])
            return evaluation.convert_condition_report_to_message(data)
        except Exception as e:
            pit_stop.logger.error(f"[Pit Stop] Error: {e}")
        time.sleep(1) 

if __name__ == '__main__':
    threading.Thread(target=pit_stop_interface, daemon=True).start()
    pit_stop.run(host='0.0.0.0', port=5000, debug=True)
