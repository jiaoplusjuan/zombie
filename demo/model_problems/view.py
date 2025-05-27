import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio  # 适用于旧版本兼容性

# 读取图片文件
def load_image(path):
    """读取图片并转换为灰度图（如需）"""
    img = imageio.imread(path)
    
    # 如果是彩色图（RGB或RGBA），转换为灰度图
    if len(img.shape) == 3 and img.shape[2] in [3, 4]:
        # 保留数据类型，转换为灰度图（使用标准加权平均）
        weights = np.array([0.2989, 0.5870, 0.1140])  # RGB权重
        img = np.dot(img[..., :3], weights).astype(img.dtype)
    return img

for i in [1,2,4,8,16,32,64,128,256,512,1024]:
    for j in ["ours","wost", "meanvalue","meanvalue_w","meanvalue_w_r","meanvalue_r"]:
        # 读取图片文件
        img1 = load_image(f"engine/solutions/{j}_{i}.png")
        img2 = load_image("engine/solutions/wost.png")

        # 验证尺寸一致性
        if img1.shape != img2.shape:
            raise ValueError(f"图片尺寸不匹配：{img1.shape} vs {img2.shape}")

        # 数据类型转换（避免溢出）
        img1_float = img1.astype("float64")
        img2_float = img2.astype("float64")

        # 计算差异
        difference = img2_float - img1_float

        # 计算MSE和PSNR（补充常用指标）
        mse = np.mean(difference**2)
        psnr = 10 * np.log10((255**2)/mse) if np.max(img1) <= 255 else float('inf')
        print(f"MSE: {mse:.2f}, PSNR: {psnr:.2f} dB")

        # 可视化设置
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        cmaps = ["viridis", "viridis", "coolwarm"]
        titles = ["Image 1", "Image 2", "Difference"]

        # 归一化函数（处理不同数据范围）
        def normalize(data):
            if np.issubdtype(data.dtype, np.integer):
                return data / np.iinfo(data.dtype).max
            return (data - data.min()) / (data.max() - data.min())

        for ax, data, cmap, title in zip(axes, [img1, img2, difference], cmaps, titles):
            # 对差异图特殊处理：中心化颜色映射
            if title == "Difference":
                max_abs = np.max(np.abs(data))
                im = ax.imshow(data, cmap=cmap, origin="upper", 
                            vmin=-max_abs, vmax=max_abs)
            else:
                im = ax.imshow(normalize(data), cmap=cmap, origin="upper")
            ax.set_title(title)
            ax.axis("off")
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        plt.tight_layout()
        import os
        os.makedirs("compare", exist_ok=True)
        plt.savefig(f"compare/{j}_{i}.png", dpi=300, bbox_inches="tight")
        # plt.show()