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
        self.device: AdbDevice | None = None
        # 用来存储连接后的设备对象，初始为None。



    def connect(self) -> bool:
        """
        连接到指定的设备
        :return:
            bool: 连接成功返回True，失败返回False
        """
        try:
            print(f"尝试连接设备：{self.serial}...")
            # 后续self.device.* 就等价于adbutiles.device.*
            self.device = adbutils.device(serial=self.serial)

            # 检查设备是否真的在线
            if self.device.prop.model:
                print(f"成功连接到：{self.device.prop.model}")
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
            # Pillow Image -> bytes
            # adbutils给的是一个Pillow对象，而我们后续的图像处理（用OpenCV）或者保存文件，
            # 都需要的是纯粹的、格式化的图片字节流（bytes）。这个四步法就是个标准的“格式转换”流程
            # 【固定流程，可作结论】
            from io import BytesIO

            # 1. 从设备获取截图，得到一个 Pillow Image 对象
            pil_image = self.device.screenshot()

            # 2. 创建一个内存中的二进制流对象
            img_buffer = BytesIO()

            # 3. 使用Pillow的save方法，将图像以PNG格式写入到内存流中
            pil_image.save(img_buffer, format='PNG')

            # 4. 从内存流中获取完整的PNG文件的字节数据
            png_bytes = img_buffer.getvalue()
            return png_bytes

        except AdbError as e:
            print(f"Error: 截图时发生ADB错误：{e}")
            return None

        # 后续会添加click等方法，MaaTouch也会在这里进行


    def click(self, x: int, y: int):
        """
        点击操作
        :param x: 点击位置的x坐标
        :param y: 点击位置的y坐标
        """
        if not self.device:
            print("Error: 设备未连接，无法点击！")
            return

        try:
            print(f"在坐标({x}, {y})执行点击")

            # adbutils
            self.device.click(x, y)
            print("点击完成。")
        except AdbError as e:
            print(f"Error: 点击时发生adb错误：{e}")
        except Exception as e:
            print(f"Error: 点击时发生未知错误：{e}")