import time
from enum import Enum
from flask import Flask, jsonify, Response
from datetime import datetime


class Formula1Car:
    """Formula 1 Car class."""

    def __init__(self, id: int) -> None:
        """Initialize Formula 1 Car object.

        Parameters
        ----------
        id: int
            Identificator of the Formula 1 Car object.

        """
        self._id = id

    @property
    def message(self) -> dict[str, float | int | str | None]:
        """Message with the data of the Formula 1 Car.

        Returns
        -------
        self._message: dict
            Message with the data of the Formula 1 Car.

        """
        assert self._message.keys() == {'timestamp', 'id', 'velocity', 'engine_temperature',
                                        'front_right', 'front_left', 'rear_right', 'rear_left'}
        return self._message

    def get_id(self) -> int:
        """Get the id of the Formula 1 Car.

        Returns
        -------
        id: int
            Identificator of the Formula 1 Car object.

        """
        return self._id

    def set_velocity(self, velocity: float) -> None:
        """Set current velocity of the vehicle.

        Parameters
        ----------
        velocity: float
            Velocity of the vehicle provided in kilometers per hour.

        """
        assert velocity >= 0.0 and velocity <= 350.0
        self._velocity = velocity

    def get_velocity(self) -> float:
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
        min_pressure = 0.0
        max_pressure = 40.0
        if front_right:
            assert front_right >= min_pressure and front_right <= max_pressure
            self._front_right = front_right

        if front_left:
            assert front_left >= min_pressure and front_left <= max_pressure
            self._front_left = front_left

        if rear_right:
            assert rear_right >= min_pressure and rear_right <= max_pressure
            self._rear_right = rear_right

        if rear_left:
            assert rear_left >= min_pressure and rear_left <= max_pressure
            self._rear_left = rear_left

    def set_engine_temperature(self, engine_temperature: float) -> None:
        """Set current temperature of the vehicle's engine in Celsius degrees.

        Parameters
        ----------
        engine_temperature: float
            Current temperature of the vehicle's engine in Celsius degrees.

        """
        min_temp = -40.0
        max_temp = 60.0
        assert engine_temperature >= min_temp and engine_temperature <= max_temp
        self._engine_temperature = engine_temperature

    def get_engine_temperature(self) -> float:
        """Get current temperature of the vehicle's engine in Celsius degrees.

        Returns
        -------
        engine_temperature: float
            Current temperature of the vehicle's engine in Celsius degrees.

        """
        return self._engine_temperature

    def convert_data_to_message(self) -> dict:
        """Convert data to message.

        Returns
        -------
        message: dict
            Message with the data of the Formula 1 Car.

        """
        self._current_time = datetime.now.strftime("%d/%m/%Y %H:%M:%S")
        self._message['timestamp'] = self._current_time
        self._message['id'] = self._id
        self._message['velocity'] = self._velocity
        self._message['engine_temperature'] = self._engine_temperature
        self._message['front_right'] = self._front_right
        self._message['front_left'] = self._front_left
        self._message['rear_right'] = self._rear_right
        self._message['rear_left'] = self._rear_left
        return self.message


class Formula1CarStateEvaluation:
    """Formula 1 Car class."""

    def __init__(self, id: int) -> None:
        """Initialize Formula 1 Car State Evaluation object.

        Parameters
        ----------
        id: int
            Identificator of the Formula 1 Car object to be evaluated.

        """
        self._vehicle_id = id

    @property
    def vehicles_state(self) -> int:
        """State of the Formula 1 Car.

        Returns
        -------
        self._vehicles_state: int
            State of the Formula 1 Car. Possible values are: 
            0 - Normal
            1 - Warning
            2 - Fatal Error

        """
        assert self._vehicles_state in {VehicleCondition.NORMAL.value,
                                        VehicleCondition.WARNING.value,
                                        VehicleCondition.FATAL_ERROR.value}
        return self._vehicles_state


class VehicleCondition(Enum):
    """Vehicle Condition Enum."""
    NORMAL = 0
    WARNING = 1
    FATAL_ERROR = 2


class CommunicationInterface:
    """Communication Interface for Formula 1 Car."""

    def __init__(self) -> None:
        """Initialize Communication Interface object."""
        pass

    def send_message(self, message_data: dict[str, str | float | int | None]) -> Response:
        """Send Message with Formula 1 car data.

        Parameters
        ----------
        message_data: dict
            Data to be injected into the message.

        Returns
        -------
        Response
            JSON response with the message.

        """
        self._message = message_data
        return jsonify(self._message)
