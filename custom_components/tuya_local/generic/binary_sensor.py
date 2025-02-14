"""
Platform to read Tuya binary sensors.
"""
from homeassistant.components.binary_sensor import DEVICE_CLASSES, BinarySensorEntity

from ..device import TuyaLocalDevice
from ..helpers.device_config import TuyaEntityConfig
from ..helpers.mixin import TuyaLocalEntity


class TuyaLocalBinarySensor(TuyaLocalEntity, BinarySensorEntity):
    """Representation of a Tuya Binary Sensor"""

    def __init__(self, device: TuyaLocalDevice, config: TuyaEntityConfig):
        """
        Initialise the sensor.
        Args:
            device (TuyaLocalDevice): the device API instance.
            config (TuyaEntityConfig): the configuration for this entity
        """
        dps_map = self._init_begin(device, config)
        self._sensor_dps = dps_map.pop("sensor")
        if self._sensor_dps is None:
            raise AttributeError(f"{config.name} is missing a sensor dps")
        self._init_end(dps_map)

    @property
    def device_class(self):
        """Return the class of this device"""
        dclass = self._config.device_class
        if dclass in DEVICE_CLASSES:
            return dclass
        else:
            return None

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._sensor_dps.get_value(self._device)
