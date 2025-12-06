"""The OpenFlame Integration."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "openflame"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the OpenFlame component."""
    _LOGGER.info("OpenFlame is setting up!")
    # Store configuration or perform other setup tasks here
    hass.data[DOMAIN] = {} # Example: store data for your component
    return True