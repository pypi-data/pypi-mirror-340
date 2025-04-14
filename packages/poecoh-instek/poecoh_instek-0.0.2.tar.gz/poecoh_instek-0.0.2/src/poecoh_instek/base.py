from serial import Serial
import sys
from typing import overload
from time import sleep

if sys.platform == "linux":
    from serial.tools.list_ports_linux import comports
elif sys.platform == "win32":
    from serial.tools.list_ports_windows import comports
elif sys.platform == "darwin":
    from serial.tools.list_ports_osx import comports
else:
    raise Exception(f"{sys.platform} not supported.")


class InstekException(Exception):
    pass


class Status:
    ch1_cc: bool
    ch2_cc: bool
    beep: bool
    output: bool

    def __init__(self, string: str):
        self.ch1_cc = string[0] == "0"
        self.ch2_cc = string[1] == "0"
        self.beep = string[4] == "1"
        self.output = string[5] == "1"


class Identity:
    manufacturer: str
    model: str
    serial: str
    firmware: str

    def __init__(self, string: str):
        if not string.startswith("GW"):
            raise InstekException("Invalid Identity")
        strings = string.split(",")
        self.manufacturer = strings[0]
        self.model = strings[1]
        self.serial = strings[2][3:]
        self.firmware = strings[3]


class comm:
    sp: Serial

    def __init__(self, port: str, baud: int):
        self.sp = Serial(port, baud, timeout=0.08, write_timeout=0.01)

    def open(self) -> None:
        if not self.sp.is_open:
            self.sp.open()
            while not self.sp.is_open:
                sleep(0.01)

    def close(self) -> None:
        self.sp.close()

    def write(self, string: str) -> None:
        self.open()
        _ = self.sp.write(f"{string[:14]}\n".encode())
        sleep(0.01)

    def read(self, timeout: float) -> str | None:
        self.open()
        self.sp.timeout = timeout
        response = self.sp.readline().decode().strip()
        return response if len(response) else None

    def error(self) -> None:
        self.write("ERR?")
        response = self.read(timeout=1)
        if response is None:
            raise Exception("Could not get last error.")
        if response.lower() == "no error.":
            return None
        raise InstekException(response)

    def purge(self) -> None:
        try:
            _ = self.sp.read_all()
        except:
            pass
        _ = self.sp.write(b"\n")
        try:
            self.clear_errors()
            while True:
                if len(self.sp.readline()) == 0:
                    break
        except:
            pass

    def clear_errors(self) -> None:
        while True:
            try:
                self.error()
                return
            except InstekException:
                continue
            except Exception as e:
                raise e

    @overload
    def command(self, string: str) -> None: ...

    @overload
    def command(self, string: str, response: bool) -> str: ...

    def command(self, string: str, response: bool | None = None) -> str | None:
        self.write(string)
        line = self.read(timeout=0.01 if response is None else 1)
        self.error()
        if response is None or response == False:
            return None
        if line is None:
            raise InstekException("Expected response.")
        return line

    @overload
    def voltage(self, channel: int) -> float: ...

    @overload
    def voltage(self, channel: int, value: float) -> None: ...

    def voltage(self, channel: int, value: float | None = None) -> float | None:
        if value is None:
            return float(self.command(f"VOUT{channel}?", response=True)[:-1])
        self.command(f"VSET{channel}:{round(min(value, 30), 3)}")

    @overload
    def current(self, channel: int) -> float: ...

    @overload
    def current(self, channel: int, value: float) -> None: ...

    def current(self, channel: int, value: float | None = None) -> float | None:
        if value is None:
            return float(self.command(f"IOUT{channel}?", response=True)[:-1])
        self.command(f"ISET{channel}:{round(min(value, 3), 3)}")

    def status(self) -> Status:
        return Status(self.command("STATUS?", response=True))

    def identity(self) -> Identity:
        return Identity(self.command("*IDN?", response=True))

    def baud(self) -> None:
        self.command("BAUD0")
        self.sp.baudrate = 115200

    @staticmethod
    def test(port: str) -> Identity | None:
        for baud in [115200, 57600, 9600]:
            instance = comm(port, baud)
            instance.purge()
            try:
                id = instance.identity()
                instance.close()
            except:
                instance.close()
                continue
            return id
        return None


class Channel3:
    __comm: comm

    @property
    def voltage(self) -> float:
        return self.__comm.voltage(3)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self.__comm.voltage(3, min(value, 5))

    @property
    def current(self) -> float:
        return self.__comm.current(3)

    @current.setter
    def current(self, value: float) -> None:
        self.__comm.current(3, min(value, 3))

    def __init__(self, comm: comm):
        self.__comm = comm


class Channel4:
    __comm: comm

    @property
    def voltage(self) -> float:
        return self.__comm.voltage(4)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self.__comm.voltage(4, min(value, 5))

    @property
    def current(self) -> float:
        return self.__comm.current(4)

    @current.setter
    def current(self, value: float) -> None:
        self.__comm.current(4, min(value, 1))

    def __init__(self, comm: comm):
        self.__comm = comm


class ChannelI:
    __comm: comm
    __number: int

    @property
    def voltage(self) -> float:
        return self.__comm.voltage(self.__number)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self.__comm.voltage(self.__number, value)

    @property
    def current(self) -> float:
        return self.__comm.current(self.__number)

    @current.setter
    def current(self, value: float) -> None:
        self.__comm.current(self.__number, value)

    @property
    def cc(self) -> bool:
        value = getattr(self.__comm.status(), f"ch{self.__number}_cc")
        assert isinstance(value, bool)
        return value

    def __init__(self, comm: comm, number: int):
        self.__comm = comm
        self.__number = number


class ChannelS:
    __comm: comm
    __number: int

    @property
    def current(self) -> float:
        return self.__comm.current(self.__number)

    @current.setter
    def current(self, value: float) -> None:
        self.__comm.current(self.__number, value)

    def __init__(self, comm: comm, number: int):
        self.__comm = comm
        self.__number = number


class Independent:
    __comm: comm

    @property
    def ch1(self) -> ChannelI:
        return ChannelI(self.__comm, 1)

    @property
    def ch2(self) -> ChannelI:
        return ChannelI(self.__comm, 2)

    def __init__(self, comm: comm):
        comm.command("TRACK0")
        self.__comm = comm


class Series:
    __comm: comm

    @property
    def voltage(self) -> float:
        return round(self.__comm.voltage(1) * 2, 3)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self.__comm.voltage(1, value / 2)

    @property
    def current(self) -> float:
        return self.__comm.current(1)

    @current.setter
    def current(self, value: float) -> None:
        self.__comm.current(1, value)

    @property
    def cc(self) -> bool:
        return self.__comm.status().ch1_cc

    def __init__(self, comm: comm):
        comm.command("TRACK1")
        comm.current(2, 3)
        self.__comm = comm


class SeriesCommon:
    __comm: comm

    @property
    def voltage(self) -> float:
        return round(self.__comm.voltage(1) * 2, 3)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self.__comm.voltage(1, value / 2)

    @property
    def ch1(self) -> ChannelS:
        return ChannelS(self.__comm, 1)

    @property
    def ch2(self) -> ChannelS:
        return ChannelS(self.__comm, 2)

    def __init__(self, comm: comm):
        comm.command("TRACK1")
        self.__comm = comm


class Parallel:
    __comm: comm

    @property
    def voltage(self) -> float:
        return self.__comm.voltage(1)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self.__comm.voltage(1, value)

    @property
    def current(self) -> float:
        return round(self.__comm.current(1) * 2, 3)

    @current.setter
    def current(self, value: float) -> None:
        self.__comm.current(1, value / 2)

    @property
    def cc(self) -> bool:
        return self.__comm.status().ch1_cc

    def __init__(self, comm: comm):
        comm.command("TRACK2")
        self.__comm = comm
