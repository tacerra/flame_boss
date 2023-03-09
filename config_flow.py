import logging

from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv

import voluptuous as vol
from .flameBossApi import FlameBoss
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

AUTH_SCHEMA = vol.Schema(
    {vol.Required(CONF_USERNAME): cv.string, vol.Required(CONF_PASSWORD): cv.string}
)

class FlameBossConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for FlameBoss services"""

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            data = await self.async_get_entry_data(user_input, errors)
            if data:
                return await self.async_create_or_update_entry(data=data)
        
        return self.async_show_form(
            step_id="user", data_schema=AUTH_SCHEMA, errors=errors
        )

    async def async_get_entry_data(self, user_input, errors):
        try:
            client = FlameBoss()
            tokenData = await client.getToken(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            deviceId =  await client.getDeviceId()

            return {
                "user_id": tokenData["user_id"],
                "auth_token": tokenData["auth_token"],
                "username": user_input[CONF_USERNAME],
                "password": user_input[CONF_PASSWORD],
                "deviceId": deviceId,
            }
        except Exception as e:
            errors["base"] = "unknown"
            _LOGGER.exception("Unknown error")

    async def async_create_or_update_entry(self, data):
        existing_entry = await self.async_set_unique_id(f"{DOMAIN}")
        if existing_entry:
            self.hass.config_entries.async_update_entry(existing_entry, data=data)
            await self.hass.config_entries.async_reload(existing_entry.entry_id)
            return self.async_abort(reason="reauth_successful")
        return self.async_create_entry(title="Flame Boss", data=data)

    async def async_step_reauth(self, data):
        return await self.async_step_user()
