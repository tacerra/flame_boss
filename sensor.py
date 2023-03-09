from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import TEMP_FAHRENHEIT, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo

from .flameBossApi import FlameBoss
from .const import DOMAIN
from datetime import timedelta
import logging
import async_timeout

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
):
    """Set up the sensor platform."""
    sensors = []

    flameBossApi = FlameBoss(config_entry.data["username"], config_entry.data["auth_token"], config_entry.data["deviceId"])
    coordinator = MyCoordinator(hass, flameBossApi)

    sensors.append(OnlineSensor(coordinator))
    sensors.append(PitTempSensor(coordinator))
    sensors.append(PitSetTempSensor(coordinator))
    sensors.append(MeatTemp1Sensor(coordinator))
    sensors.append(MeatTemp2Sensor(coordinator))
    sensors.append(MeatTemp3Sensor(coordinator))
    sensors.append(FanSpeedSensor(coordinator))

    async_add_devices(sensors, True)

class MyCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass, flameBossApi):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="My sensor",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=30),
        )
        self.device_info = DeviceInfo(
            #entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, "location_key")},
            manufacturer="FlameBoss",
            name="Flame Boss Controller"
        )
        self.flameBossApi = flameBossApi

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            async with async_timeout.timeout(10):
                return await self.flameBossApi.getCurrentCookData()
        except ApiError as err:
            _LOGGER.error(err)
            raise UpdateFailed(f"Error communicating with API: {err}")

class OnlineSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""
    _attr_name = "Online"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["Online", "Offline"]
    _attr_unique_id = "flame_boss_online"
    
    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        self._attr_device_info = coordinator.device_info
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.coordinator.data["online"] is True:
            self._attr_native_value = "Online"
        else:
            self._attr_native_value = "Offline"

        self.async_write_ha_state()

class PitTempSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""
    _attr_name = "Pit Temp"
    _attr_native_unit_of_measurement = TEMP_FAHRENHEIT
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "flame_boss_pit_temp"

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        self._attr_device_info = coordinator.device_info
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data["pit_temp"]
        self.async_write_ha_state()

class PitSetTempSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""
    _attr_name = "Pit Set Temp"
    _attr_native_unit_of_measurement = TEMP_FAHRENHEIT
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "flame_boss_pit_set_temp"

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        self._attr_device_info = coordinator.device_info
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data["set_temp"]
        self.async_write_ha_state()

class MeatTemp1Sensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""
    _attr_name = "Meat Temp 1"
    _attr_native_unit_of_measurement = TEMP_FAHRENHEIT
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "flame_boss_meat_temp_1"

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        self._attr_device_info = coordinator.device_info
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data["meat_temp1"]
        self.async_write_ha_state()

class MeatTemp2Sensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""
    _attr_name = "Meat Temp 2"
    _attr_native_unit_of_measurement = TEMP_FAHRENHEIT
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "flame_boss_meat_temp_2"

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        self._attr_device_info = coordinator.device_info
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data["meat_temp2"]
        self.async_write_ha_state()

class MeatTemp3Sensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""
    _attr_name = "Meat Temp 3"
    _attr_native_unit_of_measurement = TEMP_FAHRENHEIT
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "flame_boss_meat_temp_3"

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        self._attr_device_info = coordinator.device_info
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data["meat_temp3"]
        self.async_write_ha_state()

class FanSpeedSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""
    _attr_name = "Fan Speed"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.POWER_FACTOR
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "flame_boss_fan_speed"

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        self._attr_device_info = coordinator.device_info
        super().__init__(coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data["fan_dc"]
        self.async_write_ha_state()

