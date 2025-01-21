"""
@Description :
读取文件，文件格式 str "[fl,fl,...]"
@Returns     :
@Author       :wuxingxing
"""
import argparse
from ftplib import error_perm
from mailbox import linesep
import math
from operator import index
import os
from turtle import color
import numpy as np
import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from pyparsing import col
from torch import rand
import seaborn as sns
from scipy.stats import linregress
picture_save_dir = "./mlff_wu_work_dir/picture_dir"

# color_list = ["#000000", "#BDB76B", "#B8860B", "#008B8B", "#FF8C00", "#A52A2A", "#5F9EA0"]
#黑，灰色，浅棕色，浅黄色，深棕色，深黄色，深绿色
# color_list = ["#000000", "#A9A9A9", "#BDB76B", "#F0E68C", "#483D8B", "#DAA520", "#008000"]
# color_list = ["#008000", "#BDB76B", "#DAA520"]
color_list = ["#800000", "#800000", "#000000", "#A52A2A"]
mark_list = [".", ",", "v", "^", "+", "o", '*']

def draw_lines(x_list:list, y_list :list, axvlines: list, legend_label, \
                      x_label, y_label, title, location, picture_save_path, draw_config = None, \
                        xticks:list=None, xtick_loc:list=None):
    # force-kpu散点图
    fontsize = 25
    fontsize2 = 25
    font =  {'family' : 'Times New Roman',
        'weight' : 'normal',
        'fontsize' : fontsize,
        }
    plt.figure(figsize=(12,10))
    plt.style.use('classic') # 画板主题风格
    plt.rcParams['font.sans-serif']=['Microsoft YaHei'] # 使用微软雅黑的字体
    # plt.grid(linewidth =1.5) # 网格线
    for i in range(len(y_list)):
        plt.plot(x_list[i], y_list[i], color=color_list[0], \
                    linewidth =3.0)
        
    for axv in axvlines:
        plt.axvline(axv, color=color_list[2], ls="--", linewidth =3.0)
    
    plt.xlim(left=0, right=max(x_list[0]))
    plt.xticks(axvlines, xticks, fontsize=fontsize2)

    plt.xticks(fontsize=fontsize2)
    plt.yticks(fontsize=fontsize2)
    plt.xlabel(x_label, font)
    # plt.yscale('log')
    # plt.xscale('log')
    plt.ylabel(y_label, font)
    plt.title(title, font)
    # 创建自定义图例
    # dft_line = mlines.Line2D([], [], color='#008000', linestyle='solid',linewidth=5)
    # # 设置图例的字体大小和颜色，以及自定义图例对象和标签
    # plt.legend(handles=[dft_line], labels=[legend_label], fontsize=15)
    plt.tight_layout()
    plt.savefig(picture_save_path)

def read_band_file(data_path):
    with open(data_path, 'r') as rf:
        lines = rf.readlines()
    x_lists =[]
    y_lists = []

    xlist = []
    ylist = []
    
    i = 3

    while i < len(lines)-1:
        if len(lines[i].split()) == 0 and len(lines[i+1].split()) == 0 and len(xlist) > 0:
            x_lists.append(xlist)
            y_lists.append(ylist)
            xlist = []
            ylist = []
        else:
            if len(lines[i].split()) > 0:
                x, y = [float(_) for _ in lines[i].split()]
                xlist.append(x)
                ylist.append(y)
        i = i + 1
    print()

    axvlines = []
    axvlines.append(0.0)
    
    lens = int(len(x_lists[0])/4)
    for i in range(1, 5):
        axvlines.append(x_lists[0][i*lens-1])
    print(axvlines)
    return x_lists, y_lists, axvlines

def draw_band(data_path, save_path, type="DFT"):
    x_lists, y_lists, axvlines = read_band_file(data_path)
    xticks = [r"$\Gamma$", "X", "M", "R", r"$\Gamma$"]
    draw_lines(x_lists, y_lists, axvlines, legend_label = type, \
        x_label = None, y_label = "Frequency (THz)", xticks=xticks, \
        title = "Phonon spectra of Si systems", location = "best", \
            picture_save_path = save_path)

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    #/share/home/wuxingxing/al_dir/cu_70/final/phy/phonopy/dft_cu/phonon_std
    #/share/home/wuxingxing/datas/al_dir/al/final/phy/phonopy/kpu_al/phonon_std
    #/share/home/wuxingxing/al_dir/si/final/phy/phonopy/dft_si_2/phonon_std
    #/share/home/wuxingxing/al_dir/si/final/phy/phonopy/kpu_si_2/phonon_std
    #/share/home/wuxingxing/al_dir/ni/final/phy/phonopy/kpu_ni/phonon_std

    parser.add_argument('-d', '--data_path', help='specify path of band.dat', type=str, default="/share/home/wuxingxing/al_dir/ni/final/phy/phonopy/kpu_ni/phonon_std/band.dat")
    parser.add_argument('-s', '--save_path', help='specify save_path', type=str, default="/share/home/wuxingxing/al_dir/ni/final/phy/phonopy/kpu_phono_ni.png")

    args = parser.parse_args()

    data_path = args.data_path
    save_path = args.save_path    
    draw_band(data_path, save_path, type="DPGEN")