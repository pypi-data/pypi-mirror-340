from peoplesoft_components import AbstractClickableComponent, GeneralLocatorStore, JsonComponent


class Button(AbstractClickableComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.BUTTON)

