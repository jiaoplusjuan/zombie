mkdir build
cd build && cmake -DFCPW_ENABLE_GPU_SUPPORT=ON .. # 如果不需要gpu则关闭DFCPW_ENABLE_GPU_SUPPORT=ON此选项
make -j4

# ./demo/demo ../demo/model_problems/engine/wost.json 


./demo_3d/demo_3d ../demo_3d/model_problems/engine/wost.json 
./demo_3d/demo_3d ../demo_3d/model_problems/engine/bvc.json
./demo_3d/demo_3d ../demo_3d/model_problems/engine/rws.json