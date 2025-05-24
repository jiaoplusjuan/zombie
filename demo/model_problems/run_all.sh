#!/bin/bash

# 颜色定义（美化输出）
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 可执行程序路径
DEMO_EXEC="./demo/demo"

# 配置文件路径前缀
CONFIG_PREFIX="../demo/model_problems/engine/wost_"
CONFIG_PREFIX2="../demo/model_problems/engine/ours_"

# 要遍历的 step 值
numsteps=(1 2 4 8 16 32 64 128 256 512 1024)

# 遍历每个 step
for step in "${numsteps[@]}"; do
    config_file="${CONFIG_PREFIX}${step}.json"
    config_file2="${CONFIG_PREFIX2}${step}.json"
    
    echo -e "${GREEN}🚀 正在运行配置文件: $config_file${NC}"
    
    # 执行命令
    "$DEMO_EXEC" "$config_file"

    echo -e "${GREEN}🚀 正在运行配置文件: $config_file2${NC}"
    # 执行命令
    "$DEMO_EXEC" "$config_file2"
    
    # 检查执行状态
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 成功完成: $step\n${NC}"
    else
        echo -e "${RED}❌ 执行失败: $step\n${NC}"
    fi
done

echo -e "${GREEN}🎉 所有步骤已处理完毕！${NC}"