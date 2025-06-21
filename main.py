import yaml
import os

from src.zzz_assistant.core.device import Device
from src.zzz_assistant.tasks.login import LoginTask
from src.zzz_assistant.utils.config_loader import load_config
from src.zzz_assistant.utils.paths import CONFIG_PATH


def main():
    """
    程序主函数
    """
    print("ZZZ Assistant 正在启动...")

    # --- 1. 加载配置 ---
    config = load_config()
    try:
        # 打印一下我们从配置文件里读到的模拟器地址和名字
        emulator_serial = config['emulator']['device_serial']
        print(f"Target emulator address: {emulator_serial}")
        print(f"Emulator name: {config['emulator']['name']}")

    except KeyError:
        print("Error: 配置文件缺少emulator.device_serial 项。")
        return
    except Exception as e:
        print(f"An error occurred while loading config: {e}")
        return  # 退出程序

    print("已成功加载配置！")


    # --- 2. 初始化核心模块 (我们后面再写) ---
    print("Initializing core modules...")
    device = Device(device_serial=emulator_serial)
    if not device.connect():
        print("Error: 无法连接到模拟器，程序退出。")
        return

    print("设备连接成功！")
    # cv_handler = ...


    # --- 3. 执行测试任务 (我们后面再写主任务) ---
    # print("Starting main task loop...")
    # run_daily_tasks(...)
    print("执行测试任务：识别主界面")
    login_task = LoginTask(device=device, config=config)
    success = login_task.run()



    print("PJSK Assistant has finished its run. (for now)")

if __name__ == '__main__':
    print("__main__主程序运行.")
    main()