from __future__ import annotations

import json
from datetime import datetime
from enum import Enum

import yaml
from flask import jsonify


class Formula1CarData:
    """Formula 1 Car class."""

    def __init__(self, id: int) -> None:
        """Initialize Formula 1 Car object.

        Parameters
        ----------
        id: int
            Identificator of the Formula 1 Car object.

        """
        self._id = id
        self._velocity = None
        self._front_right = None
        self._front_left = None
        self._rear_right = None
        self._rear_left = None
        self._engine_temperature = None
        self._current_time = None
        self._message = {
            'rear_left': self._rear_left,
            'velocity': self._velocity,
            'front_left': self._front_left,
            'front_right': self._front_right,
            'id': self._id,
            'timestamp': self._current_time,
            'engine_temperature': self._engine_temperature,
            'rear_right': self._rear_right
        }

    @property
    def message(self) -> dict[str, float | int | str | None]:
        """Message with the data of the Formula 1 Car.

        Returns
        -------
        self._message: dict
            Message with the data of the Formula 1 Car.

        """
        assert set(self._message.keys()) == {'rear_left', 'velocity', 'front_left', 'front_right',
                                             'id', 'timestamp', 'engine_temperature', 'rear_right'}
        return self._message

    def get_id(self) -> int:
        """Get the id of the Formula 1 Car.

        Returns
        -------
        id: int
            Identificator of the Formula 1 Car object.

        """
        return self._id

    def set_velocity(self, velocity: float | None) -> None:
        """Set current velocity of the vehicle.

        Parameters
        ----------
        velocity: float
            Velocity of the vehicle provided in kilometers per hour.

        """
        with open('/constants.yaml', 'r') as file:
            constants = yaml.safe_load(file)
            _max_velocity = constants[2]["velocity_limits"]["absolute_max"]
            _min_velocity = constants[2]["velocity_limits"]["absolute_min"]
            assert velocity >= _min_velocity and velocity <= _max_velocity
        self._velocity = velocity

    def get_velocity(self) -> float | None:
        """Get current velocity of the vehicle in kilometers per hour.

        Returns
        -------
        velocity: float
            Velocity of the vehicle provided in kilometers per hour.

        """
        return self._velocity

    def set_tires_pressure(self, front_right: float | None = None, front_left: float | None = None,
                           rear_right: float | None = None, rear_left: float | None = None) -> None:
        """Set tires' pressure in psi.

        Parameters
        ----------
        front_right: float
            Pressure of the front right tire in psi. Default value is None.
        front_left: float
            Pressure of the front left tire in psi. Default value is None.
        rear_right: float
            Pressure of the rear right tire in psi. Default value is None.
        rear_left: float
            Pressure of the rear left tire in psi. Default value is None.

        """
        with open('/constants.yaml', 'r') as file:
            constants = yaml.safe_load(file)
            _min_pressure = constants[1]["tires_pressure_limits"]["absolute_min"]
            _max_pressure = constants[1]["tires_pressure_limits"]["absolute_max"]

            if front_right:
                assert front_right >= _min_pressure and front_right <= _max_pressure
                self._front_right = front_right

            if front_left:
                assert front_left >= _min_pressure and front_left <= _max_pressure
                self._front_left = front_left

            if rear_right:
                assert rear_right >= _min_pressure and rear_right <= _max_pressure
                self._rear_right = rear_right

            if rear_left:
                assert rear_left >= _min_pressure and rear_left <= _max_pressure
                self._rear_left = rear_left

    def set_engine_temperature(self, engine_temperature: float) -> None:
        """Set current temperature of the vehicle's engine in Celsius degrees.

        Parameters
        ----------
        engine_temperature: float
            Current temperature of the vehicle's engine in Celsius degrees.

        """
        with open('/constants.yaml', 'r') as file:
            constants = yaml.safe_load(file)
            _min_temp = constants[0]["engine_temp_limits"]["absolute_min"]
            _max_temp = constants[0]["engine_temp_limits"]["absolute_max"]
            assert engine_temperature >= _min_temp and engine_temperature <= _max_temp
            self._engine_temperature = engine_temperature

    def get_engine_temperature(self) -> float:
        """Get current temperature of the vehicle's engine in Celsius degrees.

        Returns
        -------
        engine_temperature: float
            Current temperature of the vehicle's engine in Celsius degrees.

        """
        return self._engine_temperature

    def convert_data_to_message(self) -> dict[str, float | int | str | None]:
        """Convert data to message.

        Returns
        -------
        message: dict[str, float | int | str | None]
            Message with the data of the Formula 1 Car.

        """
        self._current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._message['timestamp'] = self._current_time
        self._message['id'] = self._id
        self._message['velocity'] = self._velocity
        self._message['engine_temperature'] = self._engine_temperature
        self._message['front_right'] = self._front_right
        self._message['front_left'] = self._front_left
        self._message['rear_right'] = self._rear_right
        self._message['rear_left'] = self._rear_left
        return jsonify(self.message)


class Formula1CarDataEvaluation:
    """Formula 1 Car class."""

    def __init__(self, id: int) -> None:
        """Initialize Formula 1 Car Data Evaluation object.

        Parameters
        ----------
        id: int
            Identificator of the Formula 1 Car object to be evaluated.

        """
        self._vehicle_id = id
        self._vehicles_condition = VehiclesCondition.NORMAL.value
        self._condition_message = {
            'id': self._vehicle_id,
            'vehicles_condition': self._vehicles_condition
        }

    @property
    def vehicles_condition(self) -> int:
        """Condition of the Formula 1 Car.

        Returns
        -------
        self._vehicles_condition: int
            Condition of the Formula 1 Car. Possible values are: 
            0 - Normal
            1 - Warning
            2 - Critical Error

        """
        assert self._vehicles_condition in {VehiclesCondition.NORMAL.value,
                                        VehiclesCondition.WARNING.value,
                                        VehiclesCondition.CRITICAL_ERROR.value}
        return self._vehicles_condition

    @property
    def condition_message(self) -> dict[str, int]:
        """Condition message of the Formula 1 Car.

        Returns
        -------
        self._condition_message: dict[str, int]
            Condition message of the Formula 1 Car.

        """
        assert set(self._condition_message.keys()) == {'id', 'vehicles_condition'}
        return self._condition_message

    def evaluate_vehicle_condition(self, vehicle_data: json) -> dict[str, int]:
        """Evaluate the condition of the Formula 1 Car.

        Parameters
        ----------
        vehicle_data: Formula1CarData
            Data of the Formula 1 Car to be evaluated.

        """
        with open('/constants.yaml', 'r') as file:
            constants = yaml.safe_load(file)
            _critical_flag_min_pressure = constants[1]["tires_pressure_limits"]["critical_flag_min"]
            _warning_flag_min_pressure = constants[1]["tires_pressure_limits"]["warning_flag_min"]
            _warning_flag_max_pressure = constants[1]["tires_pressure_limits"]["warning_flag_max"]
            _critical_flag_max_pressure = constants[1]["tires_pressure_limits"]["critical_flag_max"]
            _warning_flag_max_velocity = constants[2]["velocity_limits"]["warning_flag_max"]
            _critical_flag_min_engine_temperature = constants[0]["engine_temp_limits"]["critical_flag_min"]
            _warning_flag_min_engine_temperature = constants[0]["engine_temp_limits"]["warning_flag_min"]
            _warning_flag_max_engine_temperature = constants[0]["engine_temp_limits"]["warning_flag_max"]
            _critical_flag_max_engine_temperature = constants[0]["engine_temp_limits"]["critical_flag_max"]

            _tires = ["front_right", "front_left", "rear_right", "rear_left"]

            if any(vehicle_data[_tire] < _critical_flag_min_pressure for _tire in _tires):
                self._vehicles_condition = VehiclesCondition.CRITICAL_ERROR.value
                return self.vehicles_condition

            elif any(vehicle_data[_tire] > _critical_flag_max_pressure for _tire in _tires):
                self._vehicles_condition = VehiclesCondition.CRITICAL_ERROR.value
                return self.vehicles_condition

            elif vehicle_data["engine_temperature"] < _critical_flag_min_engine_temperature or \
                 vehicle_data["engine_temperature"] > _critical_flag_max_engine_temperature:
                self._vehicles_condition = VehiclesCondition.CRITICAL_ERROR.value
                return self.vehicles_condition

            elif any(vehicle_data[_tire] < _warning_flag_min_pressure for _tire in _tires):
                self._vehicles_condition = VehiclesCondition.WARNING.value
                return self.vehicles_condition

            elif any(vehicle_data[_tire] > _warning_flag_max_pressure for _tire in _tires):
                self._vehicles_condition = VehiclesCondition.WARNING.value
                return self.vehicles_condition

            elif vehicle_data["engine_temperature"] < _warning_flag_min_engine_temperature or \
                 vehicle_data["engine_temperature"] > _warning_flag_max_engine_temperature:
                self._vehicles_condition = VehiclesCondition.WARNING.value
                return self.vehicles_condition

            elif vehicle_data["velocity"] > _warning_flag_max_velocity:
                self._vehicles_condition = VehiclesCondition.WARNING.value
                return self.vehicles_condition

    def convert_condition_report_to_message(self, vehicle_data: json) -> dict[str, int]:
        """Convert condition report to message.

        Parameters
        ---------- 
        vehicle_data: json
            Data of the Formula 1 Car to be evaluated.

        Returns
        -------
        message: dict[str, int]
            Message with the condition of the Formula 1 Car.

        """
        self.evaluate_vehicle_condition(vehicle_data)
        self._condition_message['id'] = self._vehicle_id
        self._condition_message['vehicles_condition'] = self.vehicles_condition
        return jsonify(self.condition_message)


class VehiclesCondition(Enum):
    """Vehicle's Condition Enum class."""
    NORMAL = 0
    WARNING = 1
    CRITICAL_ERROR = 2


class MessagesDisplay:
    def __init__(self) -> None:
        """Initialize MessagesDisplay object."""

    def display_formula_1_cars_data(self, car_data: dict[str, float | None]) -> str:
        """Display Formula 1 car's data.

        Parameters
        ----------
        car_data: Formula1CarData
            Data of the Formula 1 Car to be displayed.

        Returns
        -------
        data_log: str
            Log message with the data of the Formula 1 Car.

        """
        data_log = f"ID: {car_data["id"]}\n" \
              f"Velocity: {car_data["velocity"]} km/h\n" \
              f"Tires' Pressure:\n" \
              f"  Front Right: {car_data["front_right"]} psi\n" \
              f"  Front Left: {car_data["front_left"]} psi\n" \
              f"  Rear Right: {car_data["rear_right"]} psi\n" \
              f"  Rear Left: {car_data["rear_left"]} psi\n" \
              f"Engine's Temperature: {car_data["engine_temperature"]} °C\n"
        return data_log

    def display_formula_1_cars_condition(self, car_condition: dict[str, float | None]) -> str:
        """Display Formula 1 car's condition.

        Parameters
        ----------
        car_condition: Formula1CarDataEvaluation
            Condition of the Formula 1 Car to be displayed.

        Returns
        -------
        condition_log: str
            Log message with the condition of the Formula 1 Car.

        """
        condition_log = f"ID of the vehicle: {car_condition["id"]}\n" \
                    f"Condition of the vehicle: {VehiclesCondition(car_condition["vehicles_condition"]).name}\n"
        return condition_log
