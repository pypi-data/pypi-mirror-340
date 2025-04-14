# SPDX-FileCopyrightText: 2025-present Ben Jordan <ben@poecoh.com>
#
# SPDX-License-Identifier: MIT
from . import base
__all__ = ["find", "GPD2303", "GPD3303", "GPD4303"]


class GPD:
    __comm: base.comm
    manufacturer: str
    model: str
    serial: str
    firmware: str

    @property
    def output(self) -> bool:
        return self.__comm.status().output

    @output.setter
    def output(self, state: bool) -> None:
        self.__comm.command(f"OUT{int(state)}")

    @property
    def beep(self) -> bool:
        return self.__comm.status().beep

    @beep.setter
    def beep(self, state: bool) -> None:
        self.__comm.command(f"BEEP{int(state)}")

    @property
    def independent(self) -> base.Independent:
        return base.Independent(self.__comm)

    @property
    def series(self) -> base.Series:
        return base.Series(self.__comm)

    @property
    def series_common(self) -> base.SeriesCommon:
        return base.SeriesCommon(self.__comm)

    @property
    def parallel(self) -> base.Parallel:
        return base.Parallel(self.__comm)

    def __init__(self, port: str, identity: base.Identity | None = None):
        for baud in [115200, 57600, 9600]:
            try:
                self.__comm = base.comm(port, baud)
                if identity is None:
                    self.__comm.purge()
                    identity = self.__comm.identity()
                self.__comm.baud()
                self.manufacturer = identity.manufacturer
                self.model = identity.model
                self.serial = identity.serial
                self.firmware = identity.firmware
                return
            except:
                self.__comm.close()
                continue
        raise base.InstekException("Failed to instantiate port")

    def close(self) -> None:
        self.__comm.close()

class GPD2303(GPD):
    pass


class GPD3303(GPD):
    pass


class GPD4303(GPD):
    @property
    def ch3(self) -> base.Channel3:
        return base.Channel4(self.__comm)

    @property
    def ch4(self) -> base.Channel4:
        return base.Channel4(self.__comm)


model_map: dict[str, GPD2303 | GPD3303 | GPD4303] = {
    "GPD-2303S": GPD2303,
    "GPD-3303S": GPD3303,
    "GPD-4303S": GPD4303,
}


def find() -> list[GPD2303 | GPD3303 | GPD4303]:
    found: list[GPD2303 | GPD3303 | GPD4303] = []
    for port_info in base.comports():
        if port_info.manufacturer != "FTDI":
            continue
        if base.sys.platform == "win32":
            port_id = port_info.device
        elif base.sys.platform == "linux":
            port_id = f"/dev/{port_info.name}"
        elif base.sys.platform == "darwin":
            port_id = f"/dev/{port_info.name}"
        try:
            id = base.comm.test(port_id)
            if id is None:
                continue
            cls = model_map[id.model]
            instance: GPD = cls(port_id, id)
            instance.close()
            found.append(instance)
        except:
            pass
    return found
