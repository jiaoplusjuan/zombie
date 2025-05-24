import cv2
import numpy as np
import argparse

def calculate_image_difference(path1, path2, output_diff=None):
    # 读取图像
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    if img1 is None or img2 is None:
        raise ValueError("无法加载一张或多张图像，请检查路径是否正确")

    if img1.shape != img2.shape:
        raise ValueError("两张图像尺寸不一致，无法比较")

    # 转为浮点型以便计算
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)

    # 计算差值
    diff = np.abs(img1 - img2).astype(np.uint8)

    # 计算 L2 误差（RMSE）
    mse = np.mean((img1 - img2) ** 2)
    rmse = np.sqrt(mse)

    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")

    # # 显示图像
    # cv2.imshow('Reference', img1.astype(np.uint8))
    # cv2.imshow('Approximate', img2.astype(np.uint8))
    # cv2.imshow('Difference', diff)

    if output_diff:
        cv2.imwrite(output_diff, diff)
        print(f"差值图已保存到: {output_diff}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="计算两张图像的差值并显示")
    parser.add_argument("--image1", "-i1", type=str, required=True, help="第一张图像路径（参考图）")
    parser.add_argument("--image2", "-i2", type=str, required=True, help="第二张图像路径（待比较图）")
    parser.add_argument("--output", "-o", type=str, default=None, help="保存差值图的路径（可选）")

    args = parser.parse_args()

    calculate_image_difference(args.image1, args.image2, args.output)
