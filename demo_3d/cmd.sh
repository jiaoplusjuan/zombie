mkdir build
cd build && cmake -DFCPW_ENABLE_GPU_SUPPORT=ON ..
make -j4

./demo/demo ../demo/model_problems/engine/wost.json 
./demo/demo ../demo/model_problems/engine/bvc.json
./demo/demo ../demo/model_problems/engine/rws.json