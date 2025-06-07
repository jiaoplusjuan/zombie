import os
from PIL import Image
import re

def merge_images(input_dir, output_path="combined.png"):
    # 获取所有 X=*.png 文件并按数值排序
    image_files = []
    for filename in os.listdir(input_dir):
        if filename.startswith("resized_X=") and filename.endswith(".png"):
            try:
                # 提取 X 的数值部分
                x_value = float(re.search(r"resized_X=([-+]?\d*\.?\d+)", filename).group(1))
                if x_value <= 0.3 and x_value >= -0.3:
                    image_files.append((x_value, filename))
            except (AttributeError, ValueError):
                continue
    
    # 按 X 值从小到大排序
    image_files.sort(key=lambda x: x[0])
    
    if not image_files:
        print("错误：未找到任何 X=*.png 文件！")
        return

    # 打开所有图片
    images = []
    for x_value, filename in image_files:
        img_path = os.path.join(input_dir, filename)
        images.append(Image.open(img_path))
    
    # 检查图片尺寸是否一致
    widths, heights = zip(*(img.size for img in images))
    if len(set(widths)) > 1 or len(set(heights)) > 1:
        print("警告：图片尺寸不一致，将自动调整到最小尺寸！")
        min_width = min(widths)
        min_height = min(heights)
        images = [img.resize((min_width, min_height)) for img in images]
    
    # 创建新画布（横向排列）
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)
    new_image = Image.new('RGB', (total_width, max_height))
    
    # 拼接图片
    x_offset = 0
    for img in images:
        new_image.paste(img, (x_offset, 0))
        x_offset += img.width
    
    # 保存结果
    new_image.save(output_path)
    print(f"图片合并完成！已保存到 {output_path}")
    print(f"合并顺序（按X值从小到大）：{[x[0] for x in image_files]}")

# 使用示例
if __name__ == "__main__":
    nwalks = 2
    input_dir = f"resized_slices/128_n_walks={nwalks}"  # 替换为你的文件夹路径
    if not os.path.exists("resized_combined_result"):
        os.makedirs("resized_combined_result")
    output_path = f"resized_combined_result/n_walks={nwalks}.png"   # 输出文件路径
    merge_images(input_dir, output_path)
