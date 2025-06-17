import os

from pages.base_page import BasePage
from src.zzz_assistant.utils.paths import ASSETS_PATH


class LoginPage(BasePage):
    def __init__(self, device):
        # 定义登录页面的特征：必须能看到“点击进入游戏”的按钮
        check_elements = [
            os.path.join(ASSETS_PATH, 'login', 'CLICK_INTO_GAME.png')
        ]
        super().__init__(device, "登录页", check_elements)



class MainPages(BasePage):
    def __init__(self, device):
        # 定义主页面的特征：必须能看到“导航”和“交互”按钮
        check_elements = [
            os.path.join(ASSETS_PATH, "main_page", "MAIN_GOTO_GUIDE.png"),
            os.path.join(ASSETS_PATH, "main_page", "INTERACTIVE_BUTTON.png")
        ]
        super().__init__(device, "游戏主页", check_elements)
