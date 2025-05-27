import json
import os

# 基础模板配置
base_config = {
    "solverType": "meanvalue",
    "solver": {
        "nWalks": None,  # 将被动态替换
        "maxWalkLength": 1024,
        "epsilonShellForAbsorbingBoundary": 1e-3,
        "epsilonShellForReflectingBoundary": 1e-3,
        "russianRouletteThreshold": 0.99,
        "splittingThreshold": 1.5,
        "ignoreAbsorbingBoundaryContribution": False,
        "ignoreReflectingBoundaryContribution": True,
        "ignoreSourceContribution": True,
        "runSingleThreaded": True,
        "recursive": True
    },
    "modelProblem": {
        "geometry": "demo/model_problems/engine/data/geometry.obj",
        "isReflectingBoundary": "demo/model_problems/engine/data/output_zeroed.pfm",
        "absorbingBoundaryValue": "demo/model_problems/engine/data/absorbing_boundary_value2.pfm",
        "reflectingBoundaryValue": "demo/model_problems/engine/data/reflecting_boundary_value.pfm",
        "sourceValue": "demo/model_problems/engine/data/source_value.pfm",
        "robinCoeff": 0.0,
        "absorptionCoeff": 0.0,
        "useSdfForAbsorbingBoundary": False
    },
    "output": {
        ""
        "solutionFile": None,  # 动态生成文件名
        "gridRes": 256,
        "boundaryDistanceMask": 1e-2,
        "saveDebug": False,
        "saveColormapped": True,
        "colormap": "turbo",
        "colormapMinVal": 0.0,
        "colormapMaxVal": 1.1
    }
}

# 要生成的不同 nWalks 值
n_walks_values = [1,2,4,8,16,32,64,128, 256, 512, 1024, 2048]

# 输出目录
output_dir = "engine"
os.makedirs(output_dir, exist_ok=True)

# 生成配置文件
for n_walks in n_walks_values:
    config = base_config.copy()
    
    # 深拷贝嵌套字典
    config["solver"] = base_config["solver"].copy()
    config["output"] = base_config["output"].copy()
    
    # 设置动态值
    config["solver"]["nWalks"] = n_walks
    config["output"]["solutionFile"] = f"demo/model_problems/engine/solutions/meanvalue_r_{n_walks}.pfm"
    config["output"]["csvFilename"] = f"demo/model_problems/engine/solutions/meanvalue_r_{n_walks}.csv"
    
    # 生成文件名
    filename = os.path.join(output_dir, f"meanvalue_r_{n_walks}.json")
    
    # 写入文件
    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"生成配置文件: {filename}")

