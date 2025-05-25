# 要遍历的 step 值
numsteps=(1 2 4 8 16 32 64 128 256 512 1024)

# 遍历每个 step
for step in "${numsteps[@]}"; do
    # 配置文件路径前缀
    CONFIG_PREFIX="engine/solutions/ours_"
    CONFIG_PREFIX2="engine/solutions/wost_"
    
    config_file="${CONFIG_PREFIX}${step}.csv"
    config_file2="${CONFIG_PREFIX2}${step}.csv"
    ref_file="engine/solutions/wost.csv"

    echo "🚀 正在比较: $config_file"
    
    # 执行命令
    python diff_csv.py --csv1 "$config_file" --csv2 "$ref_file"

    # 执行命令
    python diff_csv.py --csv1 "$config_file2" --csv2 "$ref_file"
    
done