import numpy as np
from scipy.ndimage import zoom

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


# 输入输出路径
input_pfm = "/home/tony/workspace/tsinghua/wos/zombie/demo/model_problems/engine/data/is_reflecting_boundary.pfm"
output_pfm = "output_half_size.pfm"

# 1️⃣ 读取 PFM 文件
data, scale, color = read_pfm(input_pfm)

# 2️⃣ 如果是彩色图，只保留第一个通道（假设其他通道一致）
if len(data.shape) == 3 and data.shape[2] == 3:
    data = data[:, :, 0]

# 3️⃣ 缩放图像（长宽各缩小为原来的一半）
zoom_factor = 0.5
resized_data = zoom(data, zoom=zoom_factor, order=1)  # order=1 表示双线性插值

# 4️⃣ 恢复为 (H, W, 1) 的形状（便于统一写入）
resized_data = resized_data[..., np.newaxis]

# 5️⃣ 写入新的 PFM 文件
write_pfm(output_pfm, resized_data, scale=scale, color=False)

print(f"✅ 缩小后的 PFM 文件已保存到: {output_pfm}")