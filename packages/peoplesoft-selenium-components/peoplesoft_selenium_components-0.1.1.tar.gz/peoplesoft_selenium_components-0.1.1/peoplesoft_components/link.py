from peoplesoft_components import AbstractClickableComponent, GeneralLocatorStore, JsonComponent


class Link(AbstractClickableComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.LINK)
