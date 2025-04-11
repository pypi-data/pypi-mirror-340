from peoplesoft_components import AbstractInputComponent, GeneralLocatorStore, JsonComponent


class TextInput(AbstractInputComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.TEXT_INPUT)

    def set_value(self, value: str):
        self.root_element.send_keys(value)
