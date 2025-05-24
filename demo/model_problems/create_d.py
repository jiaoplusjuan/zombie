import numpy as np

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
main_pfm = "engine/data/absorbing_boundary_value.pfm"  # 你当前处理后的 PFM 文件
boundary_pfm = "engine/data/output_half_size.pfm"
output_pfm = "engine/data/absorbing_boundary_value2.pfm"

# 1️⃣ 读取主 PFM 文件（假设是填充后的数据）
main_data, main_scale, main_color = read_pfm(main_pfm)

# 如果是彩色图，取第一个通道
if len(main_data.shape) == 3:
    main_data = main_data[:, :, 0]

# 2️⃣ 读取 is_reflecting_boundary.pfm 文件
boundary_data, boundary_scale, boundary_color = read_pfm(boundary_pfm)

# 同样处理颜色图
if len(boundary_data.shape) == 3:
    boundary_data = boundary_data[:, :, 0]

# 3️⃣ 检查尺寸是否一致
assert main_data.shape == boundary_data.shape, "两个 PFM 文件的尺寸必须一致！"

# 4️⃣ 对 boundary_data 乘以 0.2，并相加，大于1的部分截断成1
combined_data = np.clip(main_data * 0.8+ boundary_data * 0.4, 0, 0.99)
# combined_data = main_data + boundary_data * 0.2
# 统计combined_data中大于1的部分
print(f"combined_data 中大于1的部分数量: {np.sum(combined_data > 1)}")
# 5️⃣ 写入新文件（保持单通道）
write_pfm(output_pfm, combined_data[..., np.newaxis], scale=main_scale, color=False)

print(f"✅ 合并后的 PFM 文件已保存到: {output_pfm}")