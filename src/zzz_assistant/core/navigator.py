from pages.ad_pages import AdPage
from pages.base_page import BasePage
from pages.main_pages import LoginPage, MainPage
from src.zzz_assistant.core.device import Device


class Navigator:
    def __init__(self, device: Device):
        self.device = device

        # 【【【把所有已知的页面都注册到这里】】】
        self.known_pages: list[BasePage] = [
            LoginPage(device),
            MainPage(device),
            AdPage(device),
        ]


    def get_current_page(self, timeout: int = 10) -> BasePage | None:
        """
        识别当前屏幕处于哪个已知页面。

        它会遍历所有已知页面，并调用它们的 is_on_page 方法。
        第一个返回True的页面就是当前页面。
        """
        print("\n--- 开始识别当前页面 ---")
        for page in self.known_pages:
            if page.is_on_page(timeout=timeout):
                print(f"当前页面：{page.name}")
                return page

        print("Warning: 未能识别出当前属于任何已知页面。")
        return None
