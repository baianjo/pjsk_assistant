import os

from pages.base_page import BasePage
from src.zzz_assistant.utils.paths import ASSETS_PATH


class AdPage(BasePage):
    def __init__(self, device):
        check_elements = [
            os.path.join(ASSETS_PATH, 'login', '_TEMP_AD_BUTTON.png')
        ]
        super().__init__(device, '广告弹窗页', check_elements)