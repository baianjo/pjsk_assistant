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


    def get_current_page(self) -> BasePage | None:
        """
        识别当前屏幕处于哪个已知页面。

        只截一次图，供所有页面检查。调用它们的 is_on_page 方法。
        但由于直接传了screenshot_bytes，wait_for_template会忽略，所以设计timeout没什么用
        第一个返回True的页面就是当前页面。
        """
        print("\n--- 开始识别当前页面 ---")
        screenshot_bytes = self.device.screenshot()
        if not screenshot_bytes:
            print("Error: 获取当前页面截图失败。")
            return None


        for page in self.known_pages:
            if page.is_on_page(screenshot_bytes=screenshot_bytes):
                print(f"当前页面：{page.name}")
                return page

        print("Warning: 未能识别出当前属于任何已知页面。")
        return None
