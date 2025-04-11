from peoplesoft_components import AbstractInputComponent, GeneralLocatorStore, JsonComponent


class Checkbox(AbstractInputComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.CHECKBOX)

    def is_checked(self):
        return self.root_element.get_attribute("checked") == "checked"
