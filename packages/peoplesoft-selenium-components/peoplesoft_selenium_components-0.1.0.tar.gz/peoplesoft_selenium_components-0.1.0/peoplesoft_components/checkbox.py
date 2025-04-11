from components.abstract_input import AbstractInputComponent
from components.json_locators import GeneralLocatorStore, JsonComponent


class Checkbox(AbstractInputComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.CHECKBOX)

    def is_checked(self):
        return self.root_element.get_attribute("checked") == "checked"
