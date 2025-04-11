from components.abstract_input import AbstractInputComponent


class AbstractClickableComponent(AbstractInputComponent):
    def click(self):
        self.root_element.click()

    def click_with_spinner(self):
        self.click()
        self._wait_for_spinner()

    def click_with_save_spinner(self):
        self.click()
        self._wait_for_saved_spinner()
