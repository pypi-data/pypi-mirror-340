from typing import Optional
import warnings
import logging
from enum import Enum
import serial

logger = logging.getLogger(__name__)

class InterlockState(Enum):
    Open = 0
    Closed = 1

class OperationMode(Enum):
    CW = 1
    Pulsed = 0 
    
class AnalogControlMode(Enum):
    Power = 0
    Current = 1
    
class AnalogControl(Enum):
    Internal = 0
    External = 1

class CoherentCube:
    BAUDRATE = 19200
    CMD_ENDING = b"\r\n"
    
    def __init__(self, port: str, timeout: Optional[int] = None, write_timeout: Optional[int] = None):
        """Create a new Coherent Cube laser controller.

        Args:
            port (str): Port to connect to (e.g. "COM3").
            timeout (Optional[int], optional): Read timeout in seconds. Defaults to None.
            write_timeout (Optional[int], optional): Write timeout in seconds. Defaults to None. 
        """
        self.__ser = serial.Serial(port, baudrate=self.BAUDRATE, timeout=timeout, write_timeout=write_timeout)
        
        try:
            self._max_power = float(self.query("MAXLP")) # max laser power in mW
            self._min_power = float(self.query("MINLP")) # min laser power in mW
            self._nom_power = float(self.query("NOMP")) # nominal CW laser power in mW
        except Exception as err:
            self.__ser.close()
            raise err


    def __del__(self):
        if self.__ser.is_open:
            self.__ser.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.__ser.is_open:
            self.__ser.close()

    def open(self):
        self.__ser.open()

    def close(self):
        self.__ser.close()

    def write(self, data: str):
        """Write data to the device.

        Args:
            data (str): Data to write. `\r\n` line ending is appended if it is not provided.
        """
        data = data.encode()
        if not data.endswith(self.CMD_ENDING):
            data += self.CMD_ENDING
            
        logger.info(f"writing {data}")
        n_out = self.__ser.write(data)
        logger.debug(f"wrote {n_out} bytes")

    def read(self) -> str:
        """Read data from the device.

        Returns:
            str: Read data. `\r\n` line ending is stripped.
        """
        data = self.__ser.read_until(self.CMD_ENDING)
        logger.info(f"recieved {data}")
        return data.rstrip(self.CMD_ENDING).decode()
    
    def parse_response(self, cmd: str, response: str) -> str:
        """Parse a  response.
        For a command `X` or query `?X` most responses have the form `X=<value>`,
        Removes `X=` from the response, leaving only the value.

        Args:
            cmd (str): Command or query. For queries, the preceding `?` is stripped if present.
            response (str): Response.

        Returns:
            str: Parsed response.
        """
        cmd = cmd.lstrip("?").rstrip(self.CMD_ENDING.decode())
        return response.lstrip(f"{cmd}=")
    
    def query(self, query: str, parse: bool = True) -> str:
        """Query the device.

        Args:
            query (str): Query. `?` is prepended if is not present.
            parse (bool, optional): Parse the query response. Defaults to True.
            [See `parse_response`.]
            
        Returns:
            str: Device response.
        """
        if not query.startswith("?"):
            query = f"?{query}"
            
        self.write(query)
        resp = self.read()
        if parse:
            resp = self.parse_response(query, resp)

        return resp
    
    def set(self, cmd: str, value: Optional[str] = None, clear_buffer: bool = True):
        """Execute a command.

        Args:
            cmd (str): Command.
            value (Optional[str], optional): Value to set. Defaults to None.
            clear_buffer (bool, optional): Clears the buffer from the laser's response to the command.
        """
        # NOTE: Most commands and queries prompt a single line response from the laser.
        if value is not None:
            cmd = f"{cmd}={value}"
            
        self.write(cmd)
        if clear_buffer:
            self.read()
        
    def on(self):
        """Turn the laser on.
        """
        self.set("L", "1")
        
    def off(self):
        """Turn the laser off.
        """
        self.set("L", 0)

    def cdrh(self, enable: bool = True):
        """Set the CDR 5 second laser on delay.

        Args:
            enable (bool, optional): Enable or disable CDRH. Defaults to True.
        """
        self.set("CDRH", str(int(enable)))

    @property
    def interlock_state(self) -> InterlockState:
        """Query the interlock state.

        Returns:
            InterlockState: Present interlock state.
        """
        # The ?LCK query has two responses.
        # The first is the status, teh second is the cause.
        # Here we manually read the second response to flush the buffer.
        resp = self.query("LCK")
        return InterlockState(int(resp))
        
    def validate_power(self, power: float):
        """Validate a power value is safe.

        Args:
            power (float): Power in mW.

        Raises:
            ValueError: `power` is negative.
            RuntimeError: `power` is greater than the laser's maximum output power.
        """
        if power < 0:
            raise ValueError("`power` must be non-negative.")
        if power > self._max_power:
            raise RuntimeError("`power` is greater than the laser's maximum.")
        
        if power > self._nom_power:
            warnings.warn("`power` is above nominal.", RuntimeWarning)
        if power < self._min_power:
            warnings.warn("`power` is below minimum.", RuntimeWarning)
        
    @property
    def max_power(self) -> float:
        """Maximum laser power.

        Returns:
            float: Maximum laser power in mW.
        """
        self._max_power = float(self.query("MAXLP"))
        return self._max_power
    
    @property
    def nominal_power(self) -> float:
        """Nominal laser power in CW mode.

        Returns:
            float: Nominal laser power in CW mode in mW.
        """
        self._nom_power = float(self.query("NOMP"))
        return self._nom_power
    
    @property
    def min_power(self) -> float:
        """Minimum laser power.

        Returns:
            float: Minimum laser power in mW.
        """
        self._min_power = float(self.query("MINLP"))
        return self._min_power
        
    @property
    def current(self) -> float:
        """Query the present operating current of the laser.

        Returns:
            float: Present operating current of the laser in milliamps.
        """
        return float(self.query("C"))
    
    @property
    def power(self) -> float:
        """Present laser power.

        Returns:
            float: Laser power.
        """
        return float(self.query("SP"))

    @power.setter
    def power(self, power: float):
        """Set the laser's output power.

        Args:
            power (float): Desired power.
        """
        self.validate_power(power)
        self.set("P", str(power))

    def operation_mode(self, mode: OperationMode):
        """Set the operating mode of the laser.

        Args:
            mode (OperationMode): Desired operation mode.
        """
        self.set("CW", str(mode.value))
        
    def analog_control_mode(self, mode: AnalogControlMode):
        """Set the analog control mode of the laser.
        If in `CW` operation mode, the mode remains in `AnalogControlMode.Power` regardless of set value.

        Args:
            mode (AnalogControlMode): Desired mode.

        Raises:
            RuntimeError: If trying to set AnalogControlMode.Power while not in `pulsed` operation mode.
        """
        self.set("ANA", str(mode.value), clear_buffer=False)
        resp = self.parse_response("ANA", self.read())
        resp = AnalogControlMode(int(resp))
        if (mode is AnalogControlMode.Current) and (resp is AnalogControlMode.Power):
            raise RuntimeError("Must be in `pulsed` operation mode to set analog control mode to `power`.")

    @property
    def analog_control(self) -> AnalogControl:
        """Query the analog control source.

        Returns:
            AnalogControl: Presetn analog control source.
        """
        mode = int(self.query("EXT"))
        return AnalogControl(mode)
        
    @analog_control.setter
    def analog_control(self, mode: AnalogControl):
        """Set the analog control source.

        Args:
            mode (AnalogControl): Desired analog control source.
        """
        self.set("EXT", str(mode.value))
        
    def calibrate(self, power: float):
        """Calibrate the laser's output power.
        Only available in `Pulse` mode.
        For digital modulation this sets the laser's output power.
        For analog modulation this sets the laser's maximum output power.

        Args:
            power (float): Calibration power in mW.
        """
        # NOTE: Does not prompt a response from the laser.
        self.validate_power(power)
        self.set("CAL", str(power), clear_buffer=False)