from __future__ import annotations
from enum import Enum
from flask import jsonify, Response
from datetime import datetime


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
        assert velocity >= 0.0 and velocity <= 350.0
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
        _min_pressure = 0.0
        _max_pressure = 40.0
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
        _min_temp = -40.0
        _max_temp = 60.0
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

    @property
    def vehicles_condition(self) -> int:
        """Condition of the Formula 1 Car.

        Returns
        -------
        self._vehicles_condition: int
            Condition of the Formula 1 Car. Possible values are: 
            0 - Normal
            1 - Warning
            2 - Fatal Error

        """
        assert self._vehicles_condition in {VehiclesCondition.NORMAL.value,
                                        VehiclesCondition.WARNING.value,
                                        VehiclesCondition.FATAL_ERROR.value}
        return self._vehicles_condition


class VehiclesCondition(Enum):
    """Vehicle's Condition Enum class."""
    NORMAL = 0
    WARNING = 1
    FATAL_ERROR = 2
