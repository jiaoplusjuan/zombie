import numpy as np
import matplotlib.pyplot as plt

def read_pfm(file_path):
    with open(file_path, "rb") as f:
        header = f.readline().decode('latin-1').rstrip()
        if header not in ['PF', 'Pf']:
            raise ValueError("Invalid PFM file format.")

        color = header == 'PF'

        # Read dimensions
        dim_line = ''
        while dim_line == '':
            dim_line = f.readline().decode('latin-1').rstrip()
        width, height = map(int, dim_line.split())

        # Read scale
        scale_line = ''
        while scale_line == '':
            scale_line = f.readline().decode('latin-1').rstrip()
        scale = float(scale_line)
        endian = '<' if scale < 0 else '>'
        scale = abs(scale)

        # Read data
        buffer = np.fromfile(f, dtype=endian + 'f')
        shape = (height, width, 3) if color else (height, width)
        data = np.reshape(buffer, shape)

        # Flip image (PFM stores bottom-to-top)
        data = np.flipud(data)

        return data, scale, color

def write_pfm(file_path, data, scale=1.0, color=False):
    height, width = data.shape[:2]

    with open(file_path, "wb") as f:
        # 构造头部字符串
        header = ('PF\n' if color else 'Pf\n')
        header += f'{width} {height}\n'
        endian_scale = -scale if (np.little_endian and scale > 0) else scale
        header += f'{endian_scale}\n'

        # 先 encode 再写入
        f.write(header.encode('latin-1'))

        # Flip 数据回原始存储方向（从下到上）
        data = np.flipud(data)

        # 写入数据
        data.tofile(f)

# 示例路径
input_pfm = "/home/tony/workspace/tsinghua/wos/zombie/demo/model_problems/engine/data/is_reflecting_boundary.pfm"
output_pfm = "output_zeroed.pfm"

# 1️⃣ 读取 PFM 文件
data, scale, color = read_pfm(input_pfm)
print("Original Data Sample:\n", data[:3, :3])

# 2️⃣ 将所有值设置为 0
zero_data = np.zeros_like(data)

# 3️⃣ 写入新文件
write_pfm(output_pfm, zero_data, scale=scale, color=color)
print(f"Zeroed PFM saved to: {output_pfm}")