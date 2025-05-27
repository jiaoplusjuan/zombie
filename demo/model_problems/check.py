import pandas as pd
import numpy as np

def check_csv_data(csv_file):
    # 读取CSV文件
    df = pd.read_csv(csv_file)

    print(f"开始检查文件: {csv_file}")
    print("-" * 60)

    # 检查是否存在 NaN 值
    if df.isnull().values.any():
        print("⚠️ 警告: 数据中存在 NaN 值（空值）")
        # 可选：打印哪些位置是 NaN
        nan_positions = df[df.isnull().any(axis=1)]
        print("\n包含 NaN 的行：")
        print(nan_positions)
    else:
        print("✅ 数据中没有 NaN 值")

    print("-" * 60)

    # 检查是否有值大于1
    has_large_values = False
    for col in df.select_dtypes(include=[np.number]).columns:
        if (df[col] > 1).any():
            print(f"⚠️ 列 '{col}' 中存在大于1的值")
            has_large_values = True

    if not has_large_values:
        print("✅ 所有数值列中的值都不大于1")

# 示例调用
if __name__ == "__main__":
    csv_file = "engine/solutions/meanvalue_w_r_1.csv"  # 替换为你的CSV文件路径
    check_csv_data(csv_file)