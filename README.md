### 仓库内容说明
- 本仓库实现了我们的方法`ours`，json文件参考`zombie/demo/model_problems/engine/ours_2048.json`
   - 关键代码：
      - `zombie/include/zombie/point_estimation/ours.h`，其中实现了在WoST过程中存储相关信息
      - `zombie/include/zombie/point_estimation/common.h`，其中实现WoST过程中存储信息的基类CachesBall与CachesPoint，以及在求解过程中利用缓存点计算贡献值的函数`getEstimatedSolution`
      - `zombie/demo/demo.cpp`中，新增参数判断，选择我们的方法时调用我们的方法函数。
- 本仓库实现了`mean_value_caching`
   - `zombie/demo/demo.cpp`中，新增参数判断，选择我们的方法时调用`mean_value_caching`的方法，设置参数选择采样点、加权函数与循环轮次。
- 脚本：
   - 在`zombie/demo/model_problems`目录下有大量脚本，用于衡量mse、生成计算脚本、可视化结果等

### 运行方法示例
```
git submodule update --init --recursive
mkdir build && cd build && cmake ..
make -j4
./demo/demo ../demo/model_problems/engine/wost.json
```
