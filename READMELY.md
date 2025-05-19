# 环境配置

## **安装 Slang 和 glslang**

`FCPW_SLANG_GLSLANG_LIBRARY` 依赖于 [Slang](https://github.com/shader-slang/slang) 和 [glslang](https://github.com/KhronosGroup/glslang) 库。以下是安装方法：

在deps中git clone：

```bash
git clone https://github.com/KhronosGroup/glslang.git
cd glslang
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
sudo make install
```

```bash
git clone https://github.com/shader-slang/slang.git
cd slang
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
sudo make install
```

如果遇到问题：

* 我记得这俩库有一个要运行一个python文件才能继续（有报错提示）
* 记得递归clone子模块`git submodule update --init --recursive`

验证方式：

```bash
glslangValidator --version
slangc --version
```

# 编译命令

安装完成后，运行  demo/cmd.sh 里面的命令

## makelist修改

demo/CMakeLists.txt修改：

```bash
    target_compile_definitions(demo PRIVATE -DFCPW_USE_GPU_LUYAN)
    target_link_libraries(demo
    ${FCPW_GFX_LIBRARY}
    ${FCPW_SLANG_LIBRARY}
    ${FCPW_SLANG_GLSLANG_LIBRARY}
    ${FCPW_SLANG_RT_LIBRARY}
    )
```

修改解释：

1.引入编译开关 FCPW_USE_GPU_LUYAN，用于后续修改。这个开关的思路可以参考deps/fcpw/demos/demo.cpp 的 FCPW_USE_GPU，在deps/fcpw/demos/CMakeLists.txt里有类似修改。

2.后一句用于把上一节安装的库链接进来

# 代码框架解释

可以参考 deps/fcpw/demos/demo.cpp

从cpu到gpu主要有两方面：

1. scene到gpuscene
2. 对应的计算方法改成gpu，如Interaction变成GPUIteraction

这两方面修改可以从demo.cpp中看到，而在zombie中分别对应

1. include/zombie/utils/fcpw_geometric_queries.h（搜索scene.build找到四个地方）改动我没有commit，下面会给我的其中一个修改样例。
2. deps/fcpw/include/fcpw/fcpw.inl，需要给所有函数都+GPU前缀，并且新增对应函数接口，新增思路与类比demo

针对1的样例（忽略getscene函数，主要看20~25行）

```
  void buildAccelerationStructure(
     const std::vector<Vector2>& positions,
     const std::vector<Vector2i>& indices,
     std::function<bool(float, int)> ignoreCandidateSilhouette,
     bool buildBvh = true,
     bool enableBvhVectorization = false) {
     if (positions.size() > 0) {
         // load positions and indices
         scene.setObjectCount(1);
         scene.setObjectVertices(positions, 0);
         scene.setObjectLineSegments(indices, 0);

         // compute silhouettes
         scene.computeSilhouettes(ignoreCandidateSilhouette);

         // build aggregate
         fcpw::AggregateType aggregateType =
             buildBvh ? fcpw::AggregateType::Bvh_SurfaceArea
                      : fcpw::AggregateType::Baseline;
        #ifdef FCPW_USE_GPU_LUYAN
                scene.build(aggregateType, false, true, true);
                gpuScene.transferToGPU(scene);
        #else
                scene.build(aggregateType, enableBvhVectorization, true, true);
        #endif
     }
 }
 auto& get_scene() {
// #ifdef FCPW_USE_GPU_LUYAN
    //  return gpuScene;
// #else
     return scene;
// #endif
 }

private:
 // member
 fcpw::Scene<2> scene;
 fcpw::GPUScene<2> gpuScene;
};

```

针对2的改进

原始代码见：include/zombie/utils/fcpw_geometric_queries.h的populateGeometricQueriesForReflectingBoundary，这里思路是写了很多函数当作“工具”返回，我们重点需要修改的就是这些函数。


```cpp
template <size_t DIM, typename ReflectingBoundaryAggregateType>
void populateGeometricQueriesForReflectingBoundary(const ReflectingBoundaryAggregateType *reflectingBoundaryAggregate,
                                                   std::function<float(float)> branchTraversalWeight,
                                                   GeometricQueries<DIM>& geometricQueries)
{
    if (reflectingBoundaryAggregate) {
        geometricQueries.hasNonEmptyReflectingBoundary = true;
        geometricQueries.computeDistToReflectingBoundary = [reflectingBoundaryAggregate](
                                                           const Vector<DIM>& x, bool computeSignedDistance) -> float {
            #ifdef FCPW_USE_GPU_LUYAN
                Vector<DIM> queryPt = x;
                fcpw::GPUInteraction<DIM> interaction;
                fcpw::GPUBoundingSphere<DIM> sphere(queryPt, fcpw::maxFloat);
                reflectingBoundaryAggregate->findClosestPoint(sphere, interaction, computeSignedDistance);

                return computeSignedDistance ? interaction.signedDistance(queryPt) : interaction.d;
            #else                                      
                Vector<DIM> queryPt = x;
                fcpw::Interaction<DIM> interaction;
                fcpw::BoundingSphere<DIM> sphere(queryPt, fcpw::maxFloat);
                reflectingBoundaryAggregate->findClosestPoint(sphere, interaction, computeSignedDistance);

                return computeSignedDistance ? interaction.signedDistance(queryPt) : interaction.d;
            #endif
        };
```
