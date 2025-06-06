import adbutils
from adbutils import AdbDevice, AdbError


class Device:
    """
    设备控制器
    把所有与“设备”相关的属性（如设备序列号）和操作（如连接、截图、点击）
    都封装在这个“模具”里。以后在别的地方，我们只需要创建一个Device对象，
    就能使用所有这些功能，而不用关心底层的adb命令细节
    """

    def __init__(self, device_serial: str):
        """
        初始化设备控制器

        Args:
            device_serial (str): 设备的序列号（例如 '127.0.0.1:5555')。
                                这个值我们从config.yaml文件中获取。
        """
        self.serial: str = device_serial
        self.device: AdbDevice | None = None # 用来存储连接后的设备对象，初始为None

    def connect(self) -> bool:
        """
        连接到指定的设备
        :return:
            bool: 连接成功返回True，失败返回False
        """
        try:
            print(f"尝试连接设备：{self.serial}...")
            self.device = adbutils.device(serial=self.serial)

            #检查设备是否真的在线
            if self.device.prop.get_model():
                print(f"成功连接到：{self.device.prop.get_model()}")
                return True
            else:
                print(f"Warning: 设备{self.serial}似乎离线。")
                self.device = None
                return False

        except AdbError as e:
            print(f"Error: 连接设备时发生ADB错误：{e}")
            self.device = None
            return False
        except Exception as e:
            print(f"Error: 连接时发生未知错误：{e}")
            self.device = None
            return False


    def screenshot(self) -> bytes | None:
        """
        获取当前屏幕截图
        :return: 截图的字节数据可用于OpenCV处理，如果失败则返回None
        """
        if not self.device:
            print("Error: 设备未连接，无法截图！")
            return None

        try:
            #adbutils的screenshot()返回的是Pillow的Image对象，我们转换为OpenCV能用的格式
            #Pillow Image -> bytes
            return self.device.screenshot().tobytes()
        except AdbError as e:
            print(f"Error: 截图时发生ADB错误：{e}")
            return None

        # 后续会添加click等方法，MaaTouch也会在这里进行