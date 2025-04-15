# This file is governed by the terms outlined in the LICENSE file located in the root directory of
#  this repository. Please refer to the LICENSE file for comprehensive information.

import cryptoauthlib as cal
from ctypes import cast, c_void_p


class Connect():
    """
    Connect class to initialize and manage the connection parameters for the Secure Element interface.

    Attributes:
        device (c_void_p): Pointer to the connected device.
        interface (str): Interface type, either "I2C" or "SPI". Defaults to "I2C".
        address (str): Device address in hexadecimal format. Defaults to "0xC0".
        devtype (int): Device type, defaults to ATECC608.
        cfg (object): Configuration object for the device.

    Methods:
        __init__(**kwargs): Initializes the connection parameters.
        __connect_to_SE(): Connects to the Secure Element and initializes the device.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initializes the connection with the device.

        Args:
            **kwargs: Arbitrary keyword arguments.
                interface (str): The communication interface to use (default is "I2C").
                address (str): The device address (default is "0xC0").
                devtype (cal.ATCADeviceType): The device type (default is cal.ATCADeviceType.ATECC608).
                cfg: The configuration object (default is None).

        Attributes:
            device: The device object (initialized as None).
            interface (str): The communication interface.
            address (str): The device address.
            devtype (cal.ATCADeviceType): The device type.
            cfg: The configuration object.
        """
        self.device = None
        self.interface = kwargs.get("interface", "I2C")
        self.address = kwargs.get("address", "0xC0")
        self.devtype = kwargs.get("devtype", cal.ATCADeviceType.ATECC608)
        self.cfg = kwargs.get("cfg", None)
        if not self.cfg:
            self.cfg = cal.cfg_ateccx08a_kithid_default()
            self.cfg.devtype = int(self.devtype)
            if self.interface == "I2C":
                self.cfg.cfg.atcahid.interface = int(cal.ATCAKitType.ATCA_KIT_I2C_IFACE)
                self.cfg.cfg.atcahid.dev_identity = int(self.address, 16)
            else:
                self.cfg.cfg.atcahid.interface = int(cal.ATCAKitType.ATCA_KIT_SPI_IFACE)
        self.__connect_to_SE()

    def __connect_to_SE(self) -> None:
        """
        Establishes a connection to the SE (Secure Element) device.

        This method initializes the connection to the SE device using the provided
        configuration. It asserts that the connection is successful, otherwise it
        raises an assertion error with a message indicating the failure.

        Raises:
            AssertionError: If the connection to the SE device fails, with an error
                            message containing the error code.
        """
        status = cal.atcab_init(self.cfg)
        assert (
            status == cal.Status.ATCA_SUCCESS
        ), f"Can't connect to device... please check connections. atcab_init failed with error code 0x{status:02X}"
        self.device = cast(cal.atcab_get_device(), c_void_p)
