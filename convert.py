import os
import glob
from PIL import Image

def convert_png_to_pdf(directory):
    """
    将指定目录中的所有PNG文件转换为PDF格式
    """
    # 获取目录中所有PNG文件
    png_files = glob.glob(os.path.join(directory, "*.png"))
    
    if not png_files:
        print(f"在 {directory} 中未找到PNG文件")
        return
    
    print(f"找到 {len(png_files)} 个PNG文件，开始转换...")
    
    # 逐个转换
    for png_file in png_files:
        try:
            # 获取不带扩展名的文件名
            base_name = os.path.splitext(png_file)[0]
            pdf_file = f"{base_name}.pdf"
            
            # 打开图像并转换
            image = Image.open(png_file)
            # 如果图像模式是RGBA，需要转换为RGB以避免保存PDF时的问题
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            
            # 保存为PDF
            image.save(pdf_file, "PDF", resolution=100.0)
            print(f"已转换: {png_file} -> {pdf_file}")
            # 删除png
            # os.remove(png_file)
            
        except Exception as e:
            print(f"转换 {png_file} 时出错: {e}")
    
    print("转换完成!")

# 设置目标目录
target_directory = "/home/tony/workspace/tsinghua/wos/zombie/imgs"
convert_png_to_pdf(target_directory)