python pfm2image.py pfms /home/tony/workspace/tsinghua/wos/zombie/demo/model_problems/engine/solutions/ours_color.pfm

python pfm2image.py pfms /home/tony/workspace/tsinghua/wos/zombie/demo/model_problems/engine/solutions/wost_color.pfm


python image_diff.py --image1 engine/solutions/ours_color_1.png --image2 engine/solutions/ours_color_8.png --output difference.png