"""Platform for OpenFlame HACS Integration."""
from homeassistant.components.switch import SwitchEntity

class MySimpleSwitch(SwitchEntity):
    """Representation of a My Simple Switch."""

    def __init__(self, name):
        """Initialize the switch."""
        self._name = name
        self._state = False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        self._state = True

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        self._state = False