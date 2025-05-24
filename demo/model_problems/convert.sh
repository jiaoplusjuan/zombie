
# 要遍历的 step 值
numsteps=(1 2 4 8 16 32 64 128 256 512 1024)

# 遍历每个 step
for step in "${numsteps[@]}"; do
    # 配置文件路径前缀
    CONFIG_PREFIX="engine/solutions/ours_"
    CONFIG_PREFIX2="engine/solutions/wost_"
    
    config_file="${CONFIG_PREFIX}${step}_color.pfm"
    config_file2="${CONFIG_PREFIX2}${step}_color.pfm"
    
    echo "🚀 正在运行配置文件: $config_file"
    
    # 执行命令
    python pfm2image.py "$config_file"

    echo "🚀 正在运行配置文件: $config_file2"
    # 执行命令
    python pfm2image.py "$config_file2"
    
done

# python pfm2image.py engine/solutions/wost_color.pfm