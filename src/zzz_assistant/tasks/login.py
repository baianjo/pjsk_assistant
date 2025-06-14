import os
import yaml

from src.zzz_assistant.tasks.base_task import BaseTask
from src.zzz_assistant.utils.helpers import wait_for_template
from src.zzz_assistant.utils.paths import PROJECT_ROOT, ASSETS_PATH, CONFIG_PATH


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
        # 1. 打开游戏
        # TODO: 添加打开游戏逻辑


        # 2. 寻找并点击登录按钮
        login_button_path = os.path.join(
            ASSETS_PATH, 'login', 'CLICK_INTO_GAME.png'
        )
        login_button_location = wait_for_template(
            self.device,
            login_button_path,
            timeout=60.0)

        if not login_button_location:
            print("Error: 未在截图中找到登录按钮。")
            return False

        self.device.click(login_button_location[0], login_button_location[1])
        print("已点击登录按钮，等待进入主界面...")


        # 3. 检查该版本是否有广告，若有，等待广告标志出现
        config_path = os.path.join(CONFIG_PATH, 'config.yaml')
        ad_enabled = False
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        if config['ad']['enabled']:
            ad_enabled = True
            print("该版本有广告弹窗，等待检测并关闭")
        if ad_enabled:
            ad_button_location = wait_for_template(
                self.device,
                os.path.join(ASSETS_PATH, 'login', '_TEMP_AD_BUTTON.png'),
                timeout=60.0)
            if ad_button_location:
                self.device.click(ad_button_location[0], ad_button_location[1])
                print("已点击广告按钮，等待广告关闭...")


        # 4. 等待主界面标志出现

