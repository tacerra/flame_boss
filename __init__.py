"""The flame boss integration."""
from ctypes import cast
from datetime import timedelta
import logging
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import device_registry as dr, service
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .flameBossApi import FlameBoss
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {}).setdefault(entry.entry_id, {})

    client = FlameBoss(entry.data["username"], entry.data["auth_token"], entry.data["deviceId"])
    
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=lambda: update_data(client, entry),
        update_interval=timedelta(minutes=1),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = {
        "flame_boss_client": client,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def update_data(client: FlameBoss, entry: ConfigEntry):
    """Fetch data from API endpoint."""
    try:
        async with async_timeout.timeout(10):
            return await client.getCurrentCookData()
    except Exception as err:
        _LOGGER.error(err)
        raise UpdateFailed(f"Error communicating with API: {err}")

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok