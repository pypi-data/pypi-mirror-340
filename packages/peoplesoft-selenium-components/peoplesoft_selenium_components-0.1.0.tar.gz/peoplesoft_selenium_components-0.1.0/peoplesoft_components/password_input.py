from components.json_locators import GeneralLocatorStore, JsonComponent
from components.text_input import TextInput


class PasswordInput(TextInput):
    general_locator = GeneralLocatorStore.get(JsonComponent.PASSWORD_INPUT)