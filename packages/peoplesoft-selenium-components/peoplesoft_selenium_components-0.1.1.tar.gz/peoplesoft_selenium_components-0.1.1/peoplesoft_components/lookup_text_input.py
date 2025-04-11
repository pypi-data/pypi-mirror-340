from selenium.webdriver import Keys

from peoplesoft_components import TextInput


class LookupTextInput(TextInput):
    def set_value(self, value: str):
        self.root_element.send_keys(value + Keys.TAB)
