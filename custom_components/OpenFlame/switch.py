"""Platform for switch integration."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType = None,
) -> None:
    """Set up the My Simple Switch platform."""
    # Add your switch entities here
    add_entities([MySimpleSwitch(hass, "OpenFlame")])

class MySimpleSwitch(SwitchEntity):
    """Representation of a simple switch."""

    def __init__(self, hass: HomeAssistant, name: str) -> None:
        """Initialize the switch."""
        self._hass = hass
        self._name = name
        self._state = False  # Initial state of the switch

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._state

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        self._state = True
        self.async_write_ha_state() # Notify Home Assistant of state change

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        self._state = False
        self.async_write_ha_state() # Notify Home Assistant of state change