from components.abstract_clickable_component import AbstractClickableComponent
from components.json_locators import GeneralLocatorStore, JsonComponent


class Link(AbstractClickableComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.LINK)
