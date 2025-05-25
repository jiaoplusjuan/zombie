# 要遍历的 step 值
numsteps=(1 2 4 8 16 32 64 128 256 512 1024)

# 遍历每个 step
for step in "${numsteps[@]}"; do
    # 配置文件路径前缀
    CONFIG_PREFIX="engine/solutions/ours_"
    CONFIG_PREFIX2="engine/solutions/wost_"
    
    config_file="${CONFIG_PREFIX}${step}.pfm"
    config_file2="${CONFIG_PREFIX2}${step}.pfm"
    ref_file="engine/solutions/wost.pfm"

    config_file3="${CONFIG_PREFIX}${step}_color.pfm"
    config_file4="${CONFIG_PREFIX2}${step}_color.pfm"
    ref_file2="engine/solutions/wost_color.pfm"

    echo "🚀 正在比较: $config_file"
    
    # 执行命令
    python image_diff.py --image1 "$config_file" --image2 "$ref_file"

    # 执行命令
    python image_diff.py --image1 "$config_file2" --image2 "$ref_file"

    python image_diff.py --image1 "$config_file3" --image2 "$ref_file2"

    python image_diff.py --image1 "$config_file4" --image2 "$ref_file2"
    
done