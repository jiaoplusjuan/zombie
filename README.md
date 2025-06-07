# 3D demo

1. 根据README_ORIGIN完成zombie原始库的环境配置
2. 运行命令见 `demo_3d` 中的 `cmd_3d.sh`

## 核心代码修改

除去3d框架的整体迁移，边界硬编码可见： `demo_3d/model_problem_3d.h` 的 `pde.dirichlet` ，两个样例已经写好注释并标注TODO（方便检索）。

# 论文复现

zombie库已经实现了Boundary Value Caching与 Reverse Walk on Sphere两篇论文的代码编写。

实验报告中的超参数修改请见： `demo/model_problems/engine`中的三个.json文件，并根据实验报告进行超参数调整，该分支代码已经修改为将结果输出为csv，不会输出png效果图。

同时，在 `build_test` 中存放着部分跑好的csv结果（展示结果）。

# GPU环境配置

见README_GPU，完整库函数安装，makefile已经修改完成。
