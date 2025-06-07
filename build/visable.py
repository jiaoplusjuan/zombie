import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 读取 CSV 文件（假设文件是逗号分隔的）
file_path = "output.csv"
data = np.loadtxt(file_path, delimiter=',')

# 提取前三列（XYZ 坐标）和第四列（颜色值）
xyz = data[:, :3]  # 前三列是坐标
color_values = data[:, 3]  # 第四列是颜色值

# 将颜色值归一化到 [-1, 1]
color_min, color_max = color_values.min(), color_values.max()
print("max: ", color_max, "min: ", color_min)
# normalized_colors = 2 * (color_values - color_min) / (color_max - color_min) - 1
normalized_colors = (color_values - color_min) / (color_max - color_min)

# 过滤掉颜色值为 0 的点
mask = (color_values != 0)
print("all: ", len(xyz), "mask: ", len(xyz[mask]))
filtered_xyz = xyz[mask]
filtered_colors = normalized_colors[mask]


# 创建 3D 图形
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# 绘制散点图（颜色从蓝到红）
scatter = ax.scatter(
    filtered_xyz[:, 0], filtered_xyz[:, 1], filtered_xyz[:, 2],
    c=filtered_colors,  # 使用筛选后的颜色值
    cmap='coolwarm',      # 蓝到红的颜色映射
    vmin=0, vmax=1,      # 确保颜色范围正确
    s=10,                # 点的大小
    alpha=0.8            # 透明度
)

# 添加颜色条
cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
cbar.set_label('Normalized Color Value (0 to 1)')

# 设置坐标轴标签和标题
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Visualization of Cube Data (Blue to Red)')

# 显示图形
plt.tight_layout()
plt.show()
