from peoplesoft_components import AbstractClickableComponent, JsonComponent, GeneralLocatorStore


class Tile(AbstractClickableComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.TILE)
