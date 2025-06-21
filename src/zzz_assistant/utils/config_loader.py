import yaml
import os
from .paths import CONFIG_PATH

def load_config() -> dict:
    """
    加载配置。先加载默认配置，然后用用户配置覆盖
    """
    default_config_path = os.path.join(CONFIG_PATH, 'config.default.yaml')
    user_config_path = os.path.join(CONFIG_PATH, 'config.user.yaml')

    # 1.首先加载默认配置
    try:
        with open(default_config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print("成功加载默认配置文件。")

    except FileNotFoundError:
        print("Error: 默认配置文件config.default.yaml未找到，程序无法运行。")
        exit()
    except Exception as e:
        print(f"Error: 加载默认配置时出错：{e}")
        exit()

    # 2. 然后加载用户配置并覆盖
    if os.path.exists(user_config_path):
        try:
            with open(user_config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)

            # 使用字典的update方法来合并配置
            if user_config:
                config.update(user_config)
                print("成功加载用户配置文件，并覆盖默认设置。")
        except Exception as e:
            print(f"Warning: 加载用户配置时出错：{e}。将使用默认配置。")
    else:
        print("Warning: 用户配置文件未找到，将使用默认配置。")

    return config