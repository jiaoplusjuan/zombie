mkdir build
cd build && cmake -DFCPW_ENABLE_GPU_SUPPORT=ON ..
make -j4

./demo_3d/demo_3d ../demo_3d/model_problems/engine/wost.json 
./demo_3d/demo_3d ../demo_3d/model_problems/engine/bvc.json
./demo_3d/demo_3d ../demo_3d/model_problems/engine/rws.json