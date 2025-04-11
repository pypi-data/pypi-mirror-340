from components.base_component import BaseComponent
from components.json_locators import GeneralLocatorStore, JsonComponent


class Image(BaseComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.IMAGE)
