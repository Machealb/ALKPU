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
color_list = ["#BDB76B", "#008B8B", "#FF8C00", "#A52A2A"]
mark_list = [".", ",", "v", "^", "+", "o", '*']

def draw_lines(x_list:list, y_list :list, axvlines: list, \
               x2_list:list, y2_list :list, axvlines2: list, \
               x3_list:list = None, y3_list :list = None, axvlines3: list = None, \
                legend_label:list = None, \
                      x_label = None, y_label = None, title = None, location = None, picture_save_path = None, draw_config = None, \
                        xticks:list=None, xtick_loc:list=None):
    # force-kpu散点图
    fontsize = 35
    fontsize2 = 35
    font =  {'family' : 'Times New Roman',
        'weight' : 'normal',
        'fontsize' : fontsize,
        }
    plt.figure(figsize=(11,9))
    plt.style.use('classic') # 画板主题风格
    plt.rcParams['font.sans-serif']=['Microsoft YaHei'] # 使用微软雅黑的字体
    # plt.grid(linewidth =1.5) # 网格线
    for i in range(len(y_list)):
        plt.plot(x_list[i], y_list[i], color="#008000", \
                    linewidth =3.0)

    for i in range(len(y2_list)):
        plt.plot(x2_list[i], y2_list[i], color="#DAA520", \
                    linewidth =3.0)
        
    if x3_list is not None:
        for i in range(len(y3_list)):
            plt.plot(x3_list[i], y3_list[i], color="#800000", \
                        linewidth =3.0)
            
    for axv in axvlines2[1:-1]:
        plt.axvline(axv, color="#000000", ls="--", linewidth =3.0)

    plt.xlim(left=0, right=max(max(x_list[0]), max(x2_list[0])))

    plt.xticks(axvlines, xticks, color="#000000")

    plt.xticks(fontsize=fontsize2)
    plt.yticks(fontsize=fontsize2)
    plt.xlabel(x_label, font)
    # plt.yscale('log')
    # plt.xscale('log')
    plt.ylabel(y_label, font)
    plt.title(title, font)

    # 创建自定义图例
    # dft_patch = mpatches.Patch(color='#008000')
    dft_line = mlines.Line2D([], [], color='#008000', linestyle='solid',linewidth=5)
    kpu_line = mlines.Line2D([], [], color='#DAA520', linestyle='solid',linewidth=5)
    dpgen_line = mlines.Line2D([], [], color='#800000', linestyle='solid',linewidth=5)

    # 设置图例的字体大小和颜色，以及自定义图例对象和标签
    plt.legend(handles=[dft_line,  kpu_line, dpgen_line], \
               labels=['DFT', 'ALKPU', 'DP-GEN'], fontsize=20)
    plt.tight_layout()
    plt.savefig(picture_save_path)

def test():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import matplotlib.lines as mlines

    # 生成数据
    x = np.linspace(0, 10)
    y1 = np.sin(x)
    y2 = np.cos(x)

    # 绘图
    plt.plot(x, y1, linestyle='dashed', color='blue')
    plt.plot(x, y2, linestyle='dashed', color='red')

    # 创建自定义图例
    sin_patch = mpatches.Patch(color='blue')
    sin_line = mlines.Line2D([], [], color='blue', linestyle='dashed')
    cos_patch = mpatches.Patch(color='red')
    cos_line = mlines.Line2D([], [], color='red', linestyle='dashed')

    # 设置图例的字体大小和颜色，以及自定义图例对象和标签
    plt.legend(handles=[sin_patch, sin_line, cos_patch, cos_line], 
            labels=['sin(x) - Blue', 'cos(x) - Red'], 
            fontsize=12)

    # 显示图像
    plt.savefig("/share/home/wuxingxing/al_dir/si/final/phy/phonopy/test.png")

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

def draw_band(dft_data_path, kpu_data_path, dpgen_data_path=None, save_path=None):
    x_dft, y_dft, axv_dft = read_band_file(dft_data_path)
    x_kpu, y_kpu, axv_kpu = read_band_file(kpu_data_path)
    x_dpgen, y_dpgen, axv_dpgen = read_band_file(dpgen_data_path)
    
    xticks = [r"$\Gamma$", "X", "M", "R", r"$\Gamma$"]
    draw_lines(x_dft, y_dft, axv_dft, x_kpu, y_kpu, axv_kpu, x_dpgen, y_dpgen, axv_dpgen, legend_label = None, \
        x_label = None, y_label = "Frequency (THz)", xticks=xticks, \
        title = "Phonon spectra of Cu system", location = "best", \
            picture_save_path = save_path)

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    #/share/home/wuxingxing/al_dir/cu_70/final/phy/phonopy/dft_cu/phonon_std
    #/share/home/wuxingxing/datas/al_dir/al/final/phy/phonopy/kpu_al/phonon_std
    #/share/home/wuxingxing/al_dir/si/final/phy/phonopy/dft_si_2/phonon_std
    #/share/home/wuxingxing/al_dir/si/final/phy/phonopy/kpu_si_2/phonon_std

    # parser.add_argument('-d', '--data_path', help='specify path of band.dat', type=str, default="/share/home/wuxingxing/al_dir/si/final/phy/phonopy/dft_si_2/phonon_std/band.dat")
    # parser.add_argument('-s', '--save_path', help='specify save_path', type=str, default="/share/home/wuxingxing/al_dir/si/final/phy/phonopy/dft_si_2/phonon_std/dft_phono_si.png")

    # args = parser.parse_args()
    # si
    # dft_data_path = "/share/home/wuxingxing/al_dir/si/final/phy/phonopy/dft_si_2/phonon_std/band.dat"
    # kpu_data_path = "/share/home/wuxingxing/al_dir/si/final/phy/phonopy/kpu_si_2/phonon_std/band.dat"
    # save_path = "/share/home/wuxingxing/al_dir/si/final/phy/phonopy/phonon_si1.png" 
    # draw_band(dft_data_path, kpu_data_path, save_path)
    # test()
    # 
    # dft_data_path = "/share/home/wuxingxing/datas/al_dir/cu_3_4_70/final/phy/phonopy/dft_cu/phonon_std/band.dat"
    # kpu_data_path = "/share/home/wuxingxing/datas/al_dir/cu_3_4_70/final/phy/phonopy/kpu_cu/phonon_std/band.dat"
    # dpgen_data_path = "/share/home/wuxingxing/datas/al_dir/cu_3_4_70/final/phy/phonopy/dpgen_cu/phonon_std/band.dat"
    # save_path = "/share/home/wuxingxing/datas/al_dir/cu_3_4_70/final/phy/phonopy/phonon_cu.png" 
    # draw_band(dft_data_path, kpu_data_path, dpgen_data_path, save_path)
    
    #degree /share/home/wuxingxing/al_dir/cu_3_4_70/final/phy/phonopy/dpgen_cu_by/phonon_std
    dft_data_path = "/share/home/wuxingxing/al_dir/cu_3_4_70/final/phy/phonopy/dft_cu/phonon_std/band.dat"
    kpu_data_path = "/share/home/wuxingxing/al_dir/cu_3_4_70/final/phy/phonopy/kpu_cu_by/phonon_std/band.dat"
    dpgen_data_path = "/share/home/wuxingxing/al_dir/cu_3_4_70/final/phy/phonopy/dpgen_cu_by/phonon_std/band.dat"
    save_path = "/share/home/wuxingxing/datas/al_dir/cu_3_4_70/final/phy/phonopy/phonon_cu_by.png" 
    draw_band(dft_data_path, kpu_data_path, dpgen_data_path, save_path)

