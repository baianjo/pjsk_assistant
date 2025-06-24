from src.zzz_assistant.core.device import Device
from src.zzz_assistant.utils.helpers import wait_for_template


class BasePage:
    """
    所有页面类的基类（模具）
    name(str): 页面的唯一标识名称
    check_elements(list[str]): 用于唯一识别此页面的模板图片路径列表，只有当所有这些元素都出现时才认为在当前页面
    """
    def __init__(self, device: Device, name: str, check_elements: list[str]):
        self.device = device
        self.name = name
        self.check_elements = check_elements

    def is_on_page(self,
                   screenshot_bytes: bytes,
                   timeout: int = 2) -> bool:
        """
        检查“我”这个页面当前 **是否** 停留在屏幕上。
        通过检查所有的check_elements是否都在屏幕上出现来判断
        这是一个快速检查，所以超时时间很短
        :param timeout: 为每个元素的检查设置的超过时间
        :return: bool: 如果所有检查元素都找到则返回True，否则False
        """
        print(f"正在检查是否在【{self.name}】界面...")
        for element_path in self.check_elements:
            # 使用wait_for_template检查元素，但超时时间很短
            if not wait_for_template(self.device,
                                     element_path,
                                     timeout=timeout,
                                     pre_captured_image=screenshot_bytes):
                # 只要有一个元素没找到，就说明不在这个页面
                print(f"Error: 未找到特征【{element_path}】，判断不在【{self.name}】界面！")
                return False

        # 如果所有元素都找到，则返回True
        print(f"已确认在【{self.name}】界面.")
        return True
