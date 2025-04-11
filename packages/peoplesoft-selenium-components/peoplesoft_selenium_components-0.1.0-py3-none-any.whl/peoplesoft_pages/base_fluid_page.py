from components.nav_bar import NavBar
from pages.base_page import BasePage


class BaseFluidPage(BasePage):
    @property
    def page_title(self) -> str:
        ...

    @property
    def nav_bar(self):
        return NavBar(self.driver)
