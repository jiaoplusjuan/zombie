python pfm2image.py pfms /home/tony/workspace/tsinghua/wos/zombie/demo/model_problems/engine/solutions/ours_color.pfm

python pfm2image.py pfms /home/tony/workspace/tsinghua/wos/zombie/demo/model_problems/engine/solutions/wost_color.pfm
python pfm2image.py engine/data/output_combined.pfm

python image_diff.py --image1 engine/solutions/bvc_color.png --image2 engine/solutions/wost_old_color.png --output difference.png