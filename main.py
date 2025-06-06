import yaml
import os




def main():
    print("PJSK Assistant 正在启动...")

    # --- 1. 加载配置 ---
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print("Configuration loaded successfully.")
        # 打印一下我们从配置文件里读到的模拟器地址和名字
        print(f"Target emulator address: {config['emulator']['device_serial']}")
        print(f"Emulator name: {config['emulator']['name']}")

    except FileNotFoundError:
        print(f"Error: 无法在 {config_path} 找到配置文件！")
        return  # 退出程序
    except Exception as e:
        print(f"An error occurred while loading config: {e}")
        return  # 退出程序


    # --- 2. 初始化核心模块 (我们后面再写) ---
    print("Initializing core modules...")
    # device_controller = ...
    # cv_handler = ...


    # --- 3. 启动主任务 (我们后面再写) ---
    print("Starting main task loop...")
    # run_daily_tasks(...)


    print("PJSK Assistant has finished its run. (for now)")

if __name__ == '__main__':
    print("__main__主程序运行.")
    main()