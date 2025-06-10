import yaml
import os

from src.pjsk_assistant.core.device import Device


def main():
    """
    程序主函数
    """
    print("PJSK Assistant 正在启动...")

    # --- 1. 加载配置 ---
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print("Configuration loaded successfully.")
        # 打印一下我们从配置文件里读到的模拟器地址和名字
        emulator_serial = config['emulator']['device_serial']
        print(f"Target emulator address: {emulator_serial}")
        print(f"Emulator name: {config['emulator']['name']}")

    except FileNotFoundError:
        print(f"Error: 无法在 {config_path} 找到配置文件！")
        return  # 退出程序
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
    print("执行测试任务：截图")
    screenshot_bytes = device.screenshot()

    if screenshot_bytes:
        with open("debug_screenshot.png", "wb") as f:
            f.write(screenshot_bytes)
        print("截图成功！已保存为debug_screenshot.png")

    else:
        print("Error: 截图失败")



    print("PJSK Assistant has finished its run. (for now)")

if __name__ == '__main__':
    print("__main__主程序运行.")
    main()