from components.abstract_clickable_component import AbstractClickableComponent
from components.json_locators import JsonComponent, GeneralLocatorStore


class Tile(AbstractClickableComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.TILE)
