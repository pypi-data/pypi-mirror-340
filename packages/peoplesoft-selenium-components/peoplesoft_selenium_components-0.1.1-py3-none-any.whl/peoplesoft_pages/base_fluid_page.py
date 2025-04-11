from peoplesoft_components import NavBar
from peoplesoft_pages import BasePage


class BaseFluidPage(BasePage):
    @property
    def page_title(self) -> str:
        ...

    @property
    def nav_bar(self):
        return NavBar(self.driver)
