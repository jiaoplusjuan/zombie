
# 要遍历的 step 值
numsteps=(1 2 4 8 16 32 64 128 256 512 1024)

# 遍历每个 step
for step in "${numsteps[@]}"; do
    # 配置文件路径前缀
    CONFIG_PREFIX="engine/solutions/ours_"
    CONFIG_PREFIX2="engine/solutions/wost_"
    CONFIG_PREFIX3="engine/solutions/meanvalue_"
    CONFIG_PREFIX4="engine/solutions/meanvalue_w_"
    CONFIG_PREFIX5="engine/solutions/meanvalue_w_r_"
    CONFIG_PREFIX6="engine/solutions/meanvalue_r_"
    
    config_file="${CONFIG_PREFIX}${step}_color.pfm"
    config_file2="${CONFIG_PREFIX2}${step}_color.pfm"
    config_file3="${CONFIG_PREFIX}${step}.pfm"
    config_file4="${CONFIG_PREFIX2}${step}.pfm"
    config_file5="${CONFIG_PREFIX3}${step}_color.pfm"
    config_file6="${CONFIG_PREFIX3}${step}.pfm"
    config_file7="${CONFIG_PREFIX4}${step}_color.pfm"
    config_file8="${CONFIG_PREFIX4}${step}.pfm"
    config_file9="${CONFIG_PREFIX5}${step}_color.pfm"
    config_file10="${CONFIG_PREFIX5}${step}.pfm"
    config_file11="${CONFIG_PREFIX6}${step}_color.pfm"
    config_file12="${CONFIG_PREFIX6}${step}.pfm"
    
    echo "🚀 正在运行配置文件: $config_file"
    
    # 执行命令
    python pfm2image.py "$config_file"

    # echo "🚀 正在运行配置文件: $config_file2"
    # 执行命令
    python pfm2image.py "$config_file2"

        # echo "🚀 正在运行配置文件: $config_file3"
    
    # 执行命令
    python pfm2image.py "$config_file3"

    # echo "🚀 正在运行配置文件: $config_file4"
    # 执行命令
    python pfm2image.py "$config_file4"

    python pfm2image.py "$config_file5"

    python pfm2image.py "$config_file6"

    python pfm2image.py "$config_file7"

    python pfm2image.py "$config_file8"

    python pfm2image.py "$config_file9"

    python pfm2image.py "$config_file10"

    python pfm2image.py "$config_file11"

    python pfm2image.py "$config_file12"
    
done

python pfm2image.py engine/solutions/wost_color.pfm
python pfm2image.py engine/solutions/wost.pfm