import os
from datetime import datetime
import cv2
import numpy as np

from src.zzz_assistant.utils.paths import PROJECT_ROOT

# 定义设计分辨率为720P
DESIGN_RESOLUTION = (1280, 720) # 宽×高

def find_template(screen_image_bytes: bytes,
                  template_path: str,
                  threshold: float = 0.8,
                  debug_mode: bool = False) -> tuple[int, int] | None:
    """
    在截图中找模板图片
    :param screen_image_bytes: 从device.screenshot()获取的原始截图字节
    :param template_path: 模板图片在assets/中的路径
    :param threshold: 匹配的相似度阈值，0-1，越高越严格
    :param debug_mode: 是否开启debug模式
    :return: 如果找到，返回匹配区域中心点的坐标xy，否则返回none
    """

    try:
        # 1.将截图字节流解码为OpenCV图像格式
        screen_np = np.frombuffer(screen_image_bytes, np.uint8)
        screen_img = cv2.imdecode(screen_np, cv2.IMREAD_COLOR)


        # --- 多分辨率适配 ---
        # 2. 将实时截图缩放到我们的设计分辨率
        # 这样无论玩家用1080P还是2K屏，都是同一尺寸的图像
        h, w = screen_img.shape[:2]
        scale_ratio = DESIGN_RESOLUTION[1] / h # 按高度比例缩放
        # 把原图按计算好的比例进行缩放
        resized_screen = cv2.resize(screen_img, (int(w * scale_ratio), int(h * scale_ratio)), interpolation=cv2.INTER_AREA)


        # 3. 加载模板图片 
        with open(template_path, 'rb') as f:
            template_bytes = f.read()
        template_np = np.frombuffer(template_bytes, np.uint8)
        template_img = cv2.imdecode(template_np, cv2.IMREAD_COLOR)
        if template_img is None:
            print(f"Error: 无法加载图片at {template_path}")
            return None

        # 4. 执行模板匹配
        result = cv2.matchTemplate(resized_screen, template_img, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            # 5.如果找到了，计算中心点坐标并返回
            template_h, template_w = template_img.shape[:2]
            center_x = max_loc[0] + template_w // 2
            center_y = max_loc[1] + template_h // 2

            # <<< 如果开启了debug模式，就保存证据 >>>
            if debug_mode:
                print(f"[Debug]找到匹配！相似度为{max_val:.2f}，正在保存调试图片")

                # 在截图上画出匹配区域
                top_left = max_loc
                bottom_right = (top_left[0] + template_w, top_left[1] + template_h)

                # 用一个鲜艳的绿色矩形框标记出匹配区域，厚度为2
                cv2.rectangle(resized_screen, top_left, bottom_right, (0, 255, 0), 2)

                # 创建debug文件夹用于保存调试图片（如果不存在）
                debug_dir = os.path.join(PROJECT_ROOT, "debug")
                os.makedirs(debug_dir, exist_ok=True)

                # 生成一个独一无二的文件名
                readable_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                template_name = os.path.basename(template_path).split('.')[0]
                debug_filename = f"debug_match_{template_name}_{readable_time}.png"
                debug_filepath = os.path.join(debug_dir, debug_filename)

                # 保存带有标记的截图
                # 使用imencode来处理中文路径问题
                is_success, buffer = cv2.imencode('.png', resized_screen)
                if is_success:
                    with open(debug_filepath, 'wb') as f:
                        f.write(buffer)
                    print(f"[Debug]已保存调试图片到{debug_filepath}")
            # <<< 调试代码结束 >>>


            print(f"在坐标{(center_x, center_y)}找到模板{template_path}, 相似度：{max_val:.2f}")
            return center_x, center_y
        else:
            return None


    except Exception as e:
        print(f"Error: 匹配模板时发生错误：{e}")
        import traceback
        traceback.print_exc()
        return None


#后续我们会在这里添加颜色检测、OCR等函数




