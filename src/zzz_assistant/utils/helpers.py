import time
from src.zzz_assistant.core.device import Device
from src.zzz_assistant.core.vision import find_template


def wait_for_template(device: Device,
                      template_path: str,
                      timeout: float = 20.0,
                      interval: float = 1,
                      threshold: float = 0.9,
                      debug_mode: bool = False,
                      pre_captured_image: bytes | None = None) -> tuple[int, int] | None:
    """
    在指定时间内，周期性地等待一个模板图片出现在屏幕上。

    Args:
        device (Device): 设备控制器实例。
        template_path (str): 要寻找的模板图片的路径。
        timeout (float, optional): 最长等待时间（秒）。默认为 20.0。
        interval (float, optional): 每次检测之间的间隔时间（秒）。默认为 1.0。
        debug_mode: 使find_template函数保存一个识别范围截图
        pre_captured_image (bytes | None): 如果提供了预先捕获的截图字节，将只在该图上查找一次，忽略timeout和interval。

    Returns:
        tuple[int, int] | None: 如果在超时前找到图片，返回其中心点坐标 (x, y)；
                                如果超时仍未找到，返回 None。
    """

    # 形态一：快速检查模式 (提供 pre_captured_image)
    # 行为: 不循环不等待不超时。它只对给定的截图进行一次模板匹配，然后立刻返回结果。
    # 主要使用者: Navigator 和 Page.is_on_page()。
    #   它们需要快速地判断“此时此刻，这个东西在不在图上？”
    if pre_captured_image:
        # 如果有预截图，则直接进行一次性查找
        location = find_template(pre_captured_image, template_path)
        print(f"在预截图中查找 {'成功' if location else '失败'}")
        return location



    # 形态二：智能等待模式 (不提供 pre_captured_image)
    # 行为: 启动while 循环。它会不断地自己截图、检查，直到找到目标或者超时。
    # 主要使用者: 所有的 Task 类。
    #   比如 LoginTask 在执行完一个点击操作后，它不知道下一个界面什么时候才加载好，
    #   所以它必须调用这个模式，说：“去，给我等着那个‘主菜单’按钮出现，最多等30秒！”
    # 未来应用: 正如你预见的，以后所有的战斗、领取奖励、过剧情等任务，都会大量使用这个模式。
    print(f"开始等待图片 '{template_path.split('/')[-1]}' 出现，最长等待 {timeout} 秒...")

    start_time = time.time()
    not_found = False

    while time.time() - start_time < timeout:
        # 1. 获取截图
        screenshot_bytes = device.screenshot()
        if not screenshot_bytes:
            print("Warning: 在等待期间截图失败，0.5秒后重试...")
            time.sleep(0.5)
            continue  # 跳过本次循环，直接开始下一次

        # 2. 查找模板
        location = find_template(screenshot_bytes,
                                 template_path,
                                 threshold=threshold,
                                 debug_mode=debug_mode)
        # 等待时，可以把阈值设高一点，要求更精确
        if location:
            print(f"成功找到图片，位置：{location}。")
            return location

        # 3. 如果没找到，就等待一个间隔时间
        if not not_found:
            print(f"未找到，{interval}秒后再次检查", end='')
            not_found = True
        # 如果没找到，打印一个等待提示（可以做得更优雅，但现在够用）
        print(f".", end='', flush=True)
        print("\n")
        time.sleep(interval)

    # 4. 如果循环结束（超时了）还没返回，说明超时了
    print(f"Error: 等待图片超时（超过 {timeout} 秒）。")
    return None
