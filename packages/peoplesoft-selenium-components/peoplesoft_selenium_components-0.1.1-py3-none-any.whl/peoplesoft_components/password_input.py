from peoplesoft_components import GeneralLocatorStore, JsonComponent, TextInput


class PasswordInput(TextInput):
    general_locator = GeneralLocatorStore.get(JsonComponent.PASSWORD_INPUT)