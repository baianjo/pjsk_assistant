import os
import time

from pages.ad_pages import AdPage
from pages.main_pages import MainPage, LoginPage
from src.zzz_assistant.core.navigator import Navigator
from src.zzz_assistant.tasks.base_task import BaseTask
from src.zzz_assistant.utils.helpers import wait_for_template
from src.zzz_assistant.utils.paths import ASSETS_PATH


class LoginTask(BaseTask):
    """
    执行登录游戏到主界面的任务。使用导航器。
    继承了BaseTask，所以自动拥有了self.device和self.config
    """

    def run(self) -> bool:
        """
        重写run方法，实现登录的具体逻辑
        """
        print("开始执行【登录任务】...")
        navigator = Navigator(device=self.device)

        # 检查游戏是否运行
        print("检查游戏是否运行")
        game_package_name = self.config["game"]["package_name"]
        if not self.device.is_game_running(game_package_name):
            print(f"游戏不在前台，正在尝试启动...")
            self.device.start_game(game_package_name)
            print("游戏已启动，等待15秒后检查游戏是否启动成功...")
            time.sleep(15)


        # 从配置中获取广告处理策略
        ad_config = self.config.get('ad', {})
        ad_enabled = ad_config.get('enabled', False)
        ad_template_name = ad_config.get('template_name', '')

        if ad_enabled:
            print(f"正在处理广告：{ad_template_name}")
        else:
            print("当前版本无广告处理。如有请反馈。")


        # --- 状态机核心循环 ---
        # 设置一个总的超过时间，防止无限循环
        max_attempts = 15
        for attempt in range(max_attempts):
            print(f"\n---尝试第 {attempt + 1}/{max_attempts} 次登录---")
            current_page = navigator.get_current_page()

            if isinstance(current_page, MainPage):
                print("当前页面是主界面，登录成功！")
                return True

            elif isinstance(current_page, LoginPage):
                print("当前页面是登录界面，开始登录...")
                # 假设 LoginPage 知道如何点击自己页面上的按钮
                # self.device.click(...) 我们后续会把点击操作也封装到Page类里
                location = wait_for_template(self.device, current_page.check_elements[0])
                if location:
                    self.device.click(*location)

            elif ad_enabled and isinstance(current_page, AdPage):
                print(f"当前页面是广告界面，开始处理...")
                ad_button_path = os.path.join(ASSETS_PATH, 'login', ad_template_name)
                location = wait_for_template(self.device, ad_button_path, timeout=3)
                if location:
                    self.device.click(*location)
                    time.sleep(3)



            else: #未知界面
                print(f"当前在未知界面，可能正在加载或卡死，等待5秒后重试...")
                time.sleep(5)
                # 可以在这里加入更复杂的逻辑，比如重新启动游戏等

        print(f"Error: 经过多次尝试，仍未能到达主界面。")
        return False



