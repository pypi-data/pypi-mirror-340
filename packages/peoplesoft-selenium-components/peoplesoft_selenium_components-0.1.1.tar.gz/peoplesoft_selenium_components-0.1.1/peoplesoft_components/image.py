from peoplesoft_components import BaseComponent, GeneralLocatorStore, JsonComponent


class Image(BaseComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.IMAGE)
