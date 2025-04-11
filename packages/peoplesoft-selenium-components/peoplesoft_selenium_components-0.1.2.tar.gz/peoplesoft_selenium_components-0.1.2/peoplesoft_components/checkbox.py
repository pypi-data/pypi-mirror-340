from .abstract_input_component import AbstractInputComponent
from .json_locators import GeneralLocatorStore, JsonComponent


class Checkbox(AbstractInputComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.CHECKBOX)

    def is_checked(self):
        return self.root_element.get_attribute("checked") == "checked"
