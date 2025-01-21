import argparse
import os, glob, sys

def pick_file(movement_path, nums, save_path):
    all_num = 0
    with open(movement_path, 'r') as rf:
        lines = rf.readlines()
    for line in lines:
        if 'vector ' in line:
            all_num += 1
    config_lines = int(len(lines)/all_num)
    sample_list = list(range(0, all_num, int(all_num/nums)))
    print()
    with open(save_path, 'w') as wf:
        for s in sample_list:
            wf.writelines(lines[config_lines*s:s*config_lines+config_lines])

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--movement_path', help='specify movement_path', type=str, default="/share/home/wuxingxing/datas/system_config/al/800k/MOVEMENT")
    parser.add_argument('-n', '--nums', help='specify nums need picked', type=int, default=20)
    parser.add_argument('-s', '--save_path', help='specify save_path', type=str, default="/share/home/wuxingxing/datas/system_config/al/800k/pick_MOVEMENT")
    
    args = parser.parse_args()

    movement_path = args.movement_path
    nums = args.nums
    save_path = args.save_path
    pick_file(movement_path, nums, save_path)