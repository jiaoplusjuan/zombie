import cv2
import numpy as np
import argparse
import json
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端以避免显示窗口
def visualize_difference_matplotlib(img1, img2, output_path=None):
    """
    使用Matplotlib可视化两张图像之间的差异
    
    参数:
        img1: 第一张图像
        img2: 第二张图像
        output_path: 保存可视化结果的路径
    """
    # 确保图像是浮点型以便计算
    img1_float = img1.astype(np.float32)
    img2_float = img2.astype(np.float32)
    
    # 计算差异
    difference = img2_float - img1_float
    
    # 计算MSE
    mse = np.mean(difference ** 2)
    print(f"Mean Squared Error (MSE) between the two images: {mse:.4f}")
    
    # 转为RGB显示格式（如果是BGR格式）
    if len(img1.shape) == 3 and img1.shape[2] == 3:
        img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    else:
        img1_rgb = img1
        img2_rgb = img2
    
    # 创建可视化
    plt.figure(figsize=(15, 5))
    
    # 显示原始图像1
    plt.subplot(1, 3, 1)
    if len(img1.shape) == 3:
        plt.imshow(img1_rgb)
    else:
        plt.imshow(img1_rgb, cmap="viridis")
    plt.colorbar(label="Pixel Value")
    plt.title("原始图像")
    plt.axis('off')
    
    # 显示原始图像2
    plt.subplot(1, 3, 2)
    if len(img2.shape) == 3:
        plt.imshow(img2_rgb)
    else:
        plt.imshow(img2_rgb, cmap="viridis")
    plt.colorbar(label="Pixel Value")
    plt.title("比较图像")
    plt.axis('off')
    
    # 显示差异图像
    plt.subplot(1, 3, 3)
    # 使用coolwarm色图突出显示差异
    if len(difference.shape) == 3:
        # 对于彩色图像，计算每个通道的差异并显示强度
        diff_intensity = np.sqrt(np.sum(difference**2, axis=2))
        max_val = np.max(np.abs(diff_intensity))
        plt.imshow(diff_intensity, cmap="coolwarm", vmin=-max_val, vmax=max_val)
    else:
        max_val = np.max(np.abs(difference))
        plt.imshow(difference, cmap="coolwarm", vmin=-max_val, vmax=max_val)
    plt.colorbar(label="差异值")
    plt.title(f"差异图 (MSE: {mse:.4f})")
    plt.axis('off')
    
    plt.tight_layout()
    
    # 保存图像
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"可视化结果已保存至: {output_path}")
    
    plt.show()
    
    return mse

def calculate_image_difference(path1, path2, output_diff=None, output_json=None, visualize=False):
    """
    计算并可视化两张图像之间的差异
    
    参数:
        path1: 第一张图像的路径
        path2: 第二张图像的路径
        output_diff: 保存差异图的路径
        output_json: 保存结果的JSON文件路径
        visualize: 是否显示可视化结果
    """
    # 读取图像
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    if img1 is None or img2 is None:
        raise ValueError("无法加载一张或多张图像，请检查路径是否正确")

    if img1.shape != img2.shape:
        raise ValueError("两张图像尺寸不一致，无法比较")

    # 转为浮点型以便计算
    img1_float = img1.astype(np.float32)
    img2_float = img2.astype(np.float32)

    # 计算差值
    diff = np.abs(img1_float - img2_float).astype(np.uint8)

    # 计算 L2 误差（RMSE）
    mse = np.mean((img1_float - img2_float) ** 2)
    rmse = np.sqrt(mse)

    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")

    # 显示可视化
    # if visualize:
    vis_output = None
    if output_diff:
        vis_output = output_diff.replace('.png', '_comparison.png') if output_diff.endswith('.png') else output_diff + '_comparison.png'
        
    # 使用Matplotlib进行可视化
    visualize_difference_matplotlib(img1, img2, vis_output)
    
    # 保存差异图
    if output_diff:
        cv2.imwrite(output_diff, diff)
        print(f"差值图已保存到: {output_diff}")
    
    # 保存结果到JSON
    result = {
        path1: float(mse)
    }

    if output_json:
        existing_data = {}
        if os.path.exists(output_json):
            with open(output_json, 'r') as f:
                existing_data = json.load(f)
        
        existing_data.update(result)  # 合并新结果
        
        try:
            with open(output_json, 'w') as f:
                json.dump(existing_data, f, indent=4)
            print(f"结果已追加到 JSON 文件: {output_json}")
        except Exception as e:
            print(f"⚠️ 无法保存 JSON 文件: {str(e)}")
    
    return mse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="计算两张图像的差值并保存误差指标")
    parser.add_argument("--image1", "-i1", type=str, default="engine/solutions/wost_1024.png", help="第一张图像路径（参考图）")
    parser.add_argument("--image2", "-i2", type=str, default="engine/solutions/wost.png", help="第二张图像路径（待比较图）")
    parser.add_argument("--output_diff", "-d", type=str, default=None, help="保存差值图的路径（可选）")
    parser.add_argument("--output_json", "-j", type=str, default="diff.json", help="保存结果的JSON文件路径（可选）")
    parser.add_argument("--visualize", "-v", action="store_true", default=True, help="显示可视化结果")

    args = parser.parse_args()

    calculate_image_difference(
        args.image1, 
        args.image2, 
        args.output_diff,
        args.output_json,
        args.visualize
    )