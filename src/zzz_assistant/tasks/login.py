import os
import time

from src.zzz_assistant.tasks.base_task import BaseTask
from src.zzz_assistant.core.vision import find_template
from src.zzz_assistant.utils.paths import PROJECT_ROOT


class LoginTask(BaseTask):
    """
    执行登录游戏到主界面的任务
    继承了BaseTask，所以自动拥有了self.device和self.config
    """

    def run(self) -> bool:
        """
        重写run方法，实现登录的具体逻辑
        """
        print("开始执行【登录任务】...")
        template_path = os.path.join(
            PROJECT_ROOT,
            'assets', 'login', 'TEMPORARILY_CLOSED.png'
        )

        #尝试寻找并点击登录按钮
        screenshot_bytes = self.device.screenshot()
        if not screenshot_bytes:
            print("Error: 截图失败，登录任务终止")
            return False

        with open("debug_screenshot.png", "wb") as f:
            f.write(screenshot_bytes)
        print("【DEV】截图成功！已保存为debug_screenshot.png")


        # 调用视觉函数
        location = find_template(screenshot_bytes, template_path)
        # 根据查找结果打印信息
        if location:
            print(f"成功在坐标{location}找到了模板！即将点击此处")
            self.device.click(location[0], location[1])
            time.sleep(3)
            return True
        else:
            print("Error: 未找到模板。")
