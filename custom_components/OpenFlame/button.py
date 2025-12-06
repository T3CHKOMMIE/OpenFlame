# custom_components/your_integration_name/button.py

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    # Example: Add a single custom button
    async_add_entities([MyCustomButtonEntity()])

class MyCustomButtonEntity(ButtonEntity):
    """Representation of a custom button."""

    _attr_name = "My Custom Button" # Name displayed in Home Assistant
    _attr_unique_id = "my_custom_button_id" # Unique ID for the entity

    async def async_press(self) -> None:
        """Handle the button press."""
        # Implement the action you want to perform when the button is pressed
        # For example, call a service, send a command, or update a state
        self.hass.components.persistent_notification.async_create(
            "My Custom Button was pressed!", title="Button Pressed"
        )