import numpy as np
import argparse
import json
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib
import pandas as pd
import csv
from scipy.spatial import cKDTree
matplotlib.use('Agg')  # 使用非交互式后端以避免显示窗口

def visualize_csv_difference(data1, data2, output_path=None):
    """
    使用Matplotlib可视化两个CSV文件数据之间的差异
    
    参数:
        data1: 第一个CSV数据 (x, y, value)
        data2: 第二个CSV数据 (x, y, value)
        output_path: 保存可视化结果的路径
    """
    # 提取x, y坐标和值
    x1, y1, values1 = data1[:, 0], data1[:, 1], data1[:, 2]
    x2, y2, values2 = data2[:, 0], data2[:, 1], data2[:, 2]
    
    # 计算MSE (确保两个数据集的点是相同的)
    if np.array_equal(x1, x2) and np.array_equal(y1, y2):
        difference = values2 - values1
        mse = np.mean(difference ** 2)
        print(f"Mean Squared Error (MSE) between the two datasets: {mse:.4f}")
        rmse = np.sqrt(mse)
        print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    else:
        print("警告：两个数据集的坐标点不完全匹配，将使用最近邻插值")
        # 构建第二个数据集的KD树，用于最近邻查询
        tree = cKDTree(np.column_stack((x2, y2)))
        # 对第一个数据集中的每个点，在第二个数据集中找到最近的点
        distances, indices = tree.query(np.column_stack((x1, y1)))
        
        # 基于最近邻得到匹配的值
        matched_values2 = values2[indices]
        difference = matched_values2 - values1
        mse = np.mean(difference ** 2)
        print(f"Mean Squared Error (MSE) between the two datasets: {mse:.4f}")
        rmse = np.sqrt(mse)
        print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    
    # 创建可视化
    plt.figure(figsize=(15, 5))
    
    # 显示第一个数据集的散点图
    plt.subplot(1, 3, 1)
    scatter1 = plt.scatter(x1, y1, c=values1, cmap="viridis")
    plt.colorbar(scatter1, label="Value")
    plt.title("原始数据")
    plt.xlabel("X")
    plt.ylabel("Y")
    
    # 显示第二个数据集的散点图
    plt.subplot(1, 3, 2)
    scatter2 = plt.scatter(x2, y2, c=values2, cmap="viridis")
    plt.colorbar(scatter2, label="Value")
    plt.title("比较数据")
    plt.xlabel("X")
    plt.ylabel("Y")
    
    # 显示差异
    plt.subplot(1, 3, 3)
    # 使用匹配的点计算差异
    if np.array_equal(x1, x2) and np.array_equal(y1, y2):
        scatter_diff = plt.scatter(x1, y1, c=difference, cmap="coolwarm")
    else:
        scatter_diff = plt.scatter(x1, y1, c=difference, cmap="coolwarm")
    plt.colorbar(scatter_diff, label="Difference")
    plt.title(f"差异 (MSE: {mse:.4f})")
    plt.xlabel("X")
    plt.ylabel("Y")
    
    plt.tight_layout()
    
    # 保存图像
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"可视化结果已保存至: {output_path}")
    
    plt.close()  # 关闭图形以避免显示
    
    return mse

def load_csv_file(file_path):
    """
    加载CSV文件并提取x, y坐标和值
    
    参数:
        file_path: CSV文件路径
    返回:
        包含x, y和值的numpy数组
    """
    try:
        # 尝试使用pandas读取，这对于大多数CSV格式更加健壮
        df = pd.read_csv(file_path)
        
        # 确保CSV有至少三列
        if df.shape[1] < 3:
            raise ValueError(f"CSV文件必须至少包含3列（x, y, 值）: {file_path}")
        
        # 提取前两列作为坐标，最后一列作为值
        x = df.iloc[:, 0].to_numpy()
        y = df.iloc[:, 1].to_numpy()
        value = df.iloc[:, -1].to_numpy()
        
        return np.column_stack((x, y, value))
    
    except Exception as e:
        print(f"读取CSV文件时出错 {file_path}: {str(e)}")
        # 尝试基本的CSV解析
        data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过标题行
            for row in reader:
                if len(row) >= 3:  # 确保至少有3列
                    try:
                        x, y, value = float(row[0]), float(row[1]), float(row[-1])
                        data.append([x, y, value])
                    except ValueError:
                        continue
        
        if not data:
            raise ValueError(f"无法从CSV文件提取有效数据: {file_path}")
            
        return np.array(data)

def calculate_csv_difference(path1, path2, output_diff=None, output_json=None, visualize=False):
    """
    计算并可视化两个CSV文件中数据的差异
    
    参数:
        path1: 第一个CSV文件的路径
        path2: 第二个CSV文件的路径
        output_diff: 保存差异图的路径
        output_json: 保存结果的JSON文件路径
        visualize: 是否显示可视化结果
    """
    # 读取CSV数据
    data1 = load_csv_file(path1)
    data2 = load_csv_file(path2)

    # 输出data1中nan数据的行数
    nan_rows1 = np.isnan(data1).sum(axis=1)
    for i, row in enumerate(nan_rows1):
        if row > 0:
            print(f"data1中第 {i} 行包含 {row} 个NaN值")
    # # 判断有没有nan
    # if np.isnan(data1).any() or np.isnan(data2).any():
    #     raise ValueError("CSV文件中包含NaN值，请检查数据")



    # 计算差异
    # if np.array_equal(data1[:, :2], data2[:, :2]):  # 检查坐标是否相同
    # 跳过nan
    difference = data2[:, 2] - data1[:, 2]
    mse = np.mean(difference ** 2)
    rmse = np.sqrt(mse)
    # else:
    #     # 如果坐标不同，使用可视化函数计算MSE（它会处理不同坐标的情况）
    #     vis_output = None
    #     if output_diff:
    #         vis_output = output_diff
    #     mse = visualize_csv_difference(data1, data2, vis_output)
    #     rmse = np.sqrt(mse)
        
    #     # 已经可视化了，所以设置visualize为False
    #     visualize = False

    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")

    # 显示可视化
    if visualize:
        vis_output = None
        if output_diff:
            vis_output = output_diff
        visualize_csv_difference(data1, data2, vis_output)
    
    # 保存结果到JSON
    result = {
        path1: float(mse)
    }

    if output_json:
        existing_data = {}
        if os.path.exists(output_json):
            try:
                with open(output_json, 'r') as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                print(f"警告：JSON文件格式不正确，将创建新文件: {output_json}")
        
        existing_data.update(result)  # 合并新结果
        
        try:
            with open(output_json, 'w') as f:
                json.dump(existing_data, f, indent=4)
            print(f"结果已追加到 JSON 文件: {output_json}")
        except Exception as e:
            print(f"⚠️ 无法保存 JSON 文件: {str(e)}")
    
    return mse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="计算两个CSV文件数据的差异并保存误差指标")
    parser.add_argument("--csv1", "-c1", type=str, default="engine/solutions/data1.csv", help="第一个CSV文件路径（参考数据）")
    parser.add_argument("--csv2", "-c2", type=str, default="engine/solutions/data2.csv", help="第二个CSV文件路径（待比较数据）")
    parser.add_argument("--output_diff", "-d", type=str, default=None, help="保存差异图的路径（可选）")
    parser.add_argument("--output_json", "-j", type=str, default="diff_csv.json", help="保存结果的JSON文件路径（可选）")
    parser.add_argument("--visualize", "-v", action="store_true", default=True, help="显示可视化结果")

    args = parser.parse_args()

    calculate_csv_difference(
        args.csv1, 
        args.csv2, 
        args.output_diff,
        args.output_json,
        args.visualize
    )