import matplotlib.pyplot as plt
import numpy as np
import json
import re
import math

# 读取JSON文件
with open('diff_csv.json', 'r') as file:
    data = json.load(file)

# 创建四个数据组
groups = {
    'meanvalue': [],      # 普通均值
    'meanvalue_w': [],    # 加权均值
    'meanvalue_w_r': [],  # 加权递归
    'meanvalue_r': []     # 递归
}

# 解析数据
for key, value in data.items():
    # 只处理meanvalue相关的数据
    if not key.startswith('engine/solutions/meanvalue'):
        continue
    
    # 提取采样数
    match = re.search(r'_(\d+)\.csv$', key)
    if match:
        samples = int(match.group(1))
        
        # 根据前缀区分四组数据
        if key.startswith('engine/solutions/meanvalue_w_r_'):
            groups['meanvalue_w_r'].append((samples, value))
        elif key.startswith('engine/solutions/meanvalue_w_'):
            groups['meanvalue_w'].append((samples, value))
        elif key.startswith('engine/solutions/meanvalue_r_'):
            groups['meanvalue_r'].append((samples, value))
        elif key.startswith('engine/solutions/meanvalue_'):
            groups['meanvalue'].append((samples, value))

# 对每组数据进行排序
for group in groups:
    groups[group].sort(key=lambda x: x[0])

# 设置绘图样式
plt.figure(figsize=(10, 6))
plt.grid(True, which="both", ls="--", alpha=0.7)

# 设置颜色和标记
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
markers = ['o', 's', '^', 'D']

# 绘制每组数据
for i, (group_name, data_points) in enumerate(groups.items()):
    if not data_points:
        continue
        
    x = [point[0] for point in data_points]
    y = [point[1] for point in data_points]
    
    # 转换为log2
    log2_x = np.log2(x)
    log2_y = np.log2([max(value, 1e-10) for value in y])  # 避免log(0)
    
    # 绘制曲线
    plt.plot(log2_x, log2_y, marker=markers[i], label=group_name.replace('_', ' ').title(), 
             color=colors[i], linewidth=2, markersize=8, alpha=0.8)

# 设置图表标题和标签
plt.title('MSE vs Sample Count (Log2 Scale)', fontsize=16)
plt.xlabel('Log2(Sample Count)', fontsize=14)
plt.ylabel('Log2(MSE)', fontsize=14)
plt.legend(fontsize=12)

# 设置x轴刻度
sample_counts = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
log2_sample_counts = [math.log2(x) for x in sample_counts]
plt.xticks(log2_sample_counts, [str(x) for x in sample_counts], rotation=45)

# 美化图表
plt.tight_layout()

# 保存图表
plt.savefig('mse_vs_samples_log2.png', dpi=300, bbox_inches='tight')