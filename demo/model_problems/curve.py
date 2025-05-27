import json
import matplotlib.pyplot as plt
import numpy as np
import re

def extract_step(filename):
    """从文件名中提取步数"""
    match = re.search(r'_(\d+)\.csv', filename)
    if match:
        return int(match.group(1))
    return float('inf')  # 无效文件名放在最后

def parse_data(data):
    """解析原始数据，返回格式化数据"""
    result = {'mean_value': {}, 'mean_value_w': {}}
    
    for path, mse in data.items():
        if 'mean_value' in path and "color" not in path:
            step = extract_step(path)
            result['mean_value'][step] = mse
        elif 'mean_value_w' in path and "color" not in path:
            step = extract_step(path)
            result['mean_value_w'][step] = mse
            
    # 按步数排序
    for method in result:
        sorted_items = sorted(result[method].items())
        steps, mses = zip(*sorted_items) if sorted_items else ([], [])
        result[method] = (list(steps), list(mses))
    
    return result

def plot_results(data, output_file='mse_comparison.png'):
    """绘制对比图表"""
    plt.figure(figsize=(12, 7))
    
    # 绘制 mean_value 曲线
    if data['mean_value'][0]:
        plt.plot(data['mean_value'][0], data['mean_value'][1], 
                marker='o', label='mean_value', color='#4c72b0', linewidth=2)
    
    # 绘制 mean_value_w 曲线
    if data['mean_value_w'][0]:
        plt.plot(data['mean_value_w'][0], data['mean_value_w'][1], 
                marker='s', label='mean_value_w', color='#c44e52', linewidth=2)
    
    # 设置图表样式
    plt.title('MSE Comparison Between mean_value and mean_value_w Methods', fontsize=16)
    plt.xlabel('Number of Steps (log scale)', fontsize=14)
    plt.ylabel('Mean Squared Error (MSE)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    # 设置对数坐标
    plt.xscale('log', base=2)
    plt.yscale('log', base=2)
    plt.xticks(data['mean_value'][0] if data['mean_value'][0] else data['mean_value_w'][0], rotation=45)
    
    # 自动调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"图表已保存至: {output_file}")

def main(json_file='diff_csv.json'):
    """主函数"""
    try:
        with open(json_file, 'r') as f:
            raw_data = json.load(f)
            
        formatted_data = parse_data(raw_data)
        
        if not formatted_data['mean_value'][0] and not formatted_data['mean_value_w'][0]:
            print("未找到有效的数据点")
            return
            
        plot_results(formatted_data)
        
    except FileNotFoundError:
        print(f"错误：文件 '{json_file}' 未找到")
    except json.JSONDecodeError:
        print(f"错误：文件 '{json_file}' 不是有效的JSON格式")
    except Exception as e:
        print(f"发生未知错误: {str(e)}")

if __name__ == "__main__":
    main()