import numpy as np
import matplotlib.pyplot as plt

# 读取 CSV 文件
# file_path = "output.csv"

file_path = "../build_test/2d_output_6144rws.csv"
# file_path = "../build_test/2d_output_2048bvc.csv"
file_path="../build_test/2d_output_nwalks=128wost.csv"
data = np.loadtxt(file_path, delimiter=',')

# 提取前三列（XYZ）和第四列（颜色值）
xyz = data[:, :3]
color_values = data[:, 3]
# 交换02两列，使得数据按照 Z-Y-X 顺序排列
xyz = xyz[:, [2, 0, 1]]

# 归一化颜色值到 [-1, 1]
normalized_colors = 2 * (color_values - color_values.min()) / (color_values.max() - color_values.min()) - 1

# 选择切面的 X 值（例如 X=0，或根据数据范围调整）
x_slice = 0  # 修改为你想切的 X 值
tolerance = 0.01  # 允许的误差范围（避免因浮点数精度问题漏掉点）

# 提取切面附近的数据点
mask = np.abs(xyz[:, 0] - x_slice) < tolerance
slice_yz = xyz[mask, 1:]  # 切面的 YZ 坐标
slice_colors = normalized_colors[mask]

# 绘制切面
plt.figure(figsize=(10, 8))
scatter = plt.scatter(
    slice_yz[:, 0], slice_yz[:, 1],
    c=slice_colors,
    cmap='coolwarm',  # 蓝到红的颜色映射
    vmin=-1, vmax=1,   # 固定颜色范围
    s=20,             # 点的大小
    alpha=0.8         # 透明度
)

# 添加颜色条和标签
cbar = plt.colorbar(scatter, shrink=0.8, aspect=10)
cbar.set_label('Normalized Color Value (0 to 1)')
# plt.xlabel('Y')
# plt.ylabel('Z')
# plt.title(f'X = {x_slice} Vertical Slice (YZ Plane)')
# plt.title(file_path)

# 去除格点坐标轴 背景的所有内容都去除 + 旋转180度
plt.xticks([])
plt.yticks([])
plt.gca().set_aspect('equal', adjustable='box')
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.gca().invert_yaxis()

# 显示图形
plt.grid(True)
plt.tight_layout()
# plt.show()
fig = plt.gcf()
fig.set_size_inches(10, 8)
#输出为pdf
plt.savefig(file_path.replace('.csv', '.pdf'), dpi=300)
plt.savefig(file_path.replace('.csv', '.png'), dpi=300)


# 保存图形
# import os
# if not os.path.exists('slices'):
#     os.makedirs('slices')

# n_walks = 2
# if not os.path.exists(f'slices/128_n_walks={n_walks}'):
#     os.makedirs(f'slices/128_n_walks={n_walks}')
# png_path = os.path.join(f'slices/128_n_walks={n_walks}', f'X={x_slice}.png')
# plt.savefig(png_path, dpi=300)
