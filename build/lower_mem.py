import os
from PIL import Image
import re

def lower_mem(input_dir, output_path="combined.png"):
    # 依次打开所有图片
    images = []
    for filename in os.listdir(input_dir):
        print("Processing", filename)
        # resized_X=-0.1.png 
        if re.match(r"X=[+-]?\d+\.\d+\.png", filename):
            image = Image.open(os.path.join(input_dir, filename))
            print(f"Opened {filename}")
            # 调整图片尺寸（分辨率）
            new_size = (800, 600)  # 宽度和高度（像素）
            resized_image = image.resize(new_size)
            # 合并图片  
            images.append(resized_image)
            # 保存图片（可以设置 DPI）
            # 文件名从png变成pdf
            import img2pdf
            new_filename = os.path.join(output_path, "resized_" + filename)
            new_filename_pdf = new_filename.replace(".png", ".pdf")
            with open(new_filename_pdf, "wb") as f:
                try:
                    f.write(img2pdf.convert(new_filename))
                except Exception as e:
                    print(f"Error converting {new_filename} to PDF: {e}")
                # f.write(img2pdf.convert(resized_image))
            # resized_image.save(new_filename, dpi=(300, 300))  # 设置 DPI 为 300
            print(f"Resized {filename} to {new_size}")

def low_mem_one_file(input_file, output_path="combined.png"):
    # 打开图片
    image = Image.open(input_file)
    # 调整图片尺寸（分辨率）
    new_size = (800, 600)  # 宽度和高度（像素）
    import img2pdf
    resized_image = image.resize(new_size)
    # 保存图片（可以设置 DPI）
    # 文件名从png变成pdf
    new_filename = os.path.join(output_path, "resized_" + os.path.basename(input_file))
    new_filename_pdf = new_filename.replace(".png", ".pdf")
    with open(new_filename_pdf, "wb") as f:
        try:
            f.write(img2pdf.convert(input_file))
        except Exception as e:
            print(f"Error converting {new_filename} to PDF: {e}")
        # f.write(img2pdf.convert(resized_image))
    

# 使用示例
if __name__ == "__main__":
    # nwalks = 16
    # input_dir = f"slices/128_n_walks={nwalks}"  # 替换为你的文件夹路径
    # output_dir = f"resized_slices/128_n_walks={nwalks}"
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)
    # lower_mem(input_dir, output_dir)


    # file_name = "running_time_128.png"
    file_name = "fancy_3d.png"
    output_path = "../"
    low_mem_one_file(file_name, output_path)
