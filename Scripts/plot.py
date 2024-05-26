# Usage: python3 plot.py <path/to/file>

import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os
import numpy as np
import csv

parser = argparse.ArgumentParser()
parser.add_argument('path', type = str,
                    help = "A required string to specify the file path")
args = parser.parse_args()

file_path = args.path

def plot_cwnd(file_path):
    df = pd.read_csv(file_path, header=None, sep=' ', names=['a', 'cwnd', 'RTT'])

    # 提取第二列的值作为cwnd，第三列的值作为时间
    cwnd_values = df['cwnd']
    time_values = df['RTT']

    # 绘制cwnd随时间变化的图
    plt.figure(figsize=(10, 5))
    plt.plot(time_values, cwnd_values, marker='o')  # 使用圆点标记每个数据点
    plt.title('CWND vs RTT')
    plt.xlabel('RTT')
    plt.ylabel('CWND')
    plt.grid(True)

    # 保存图表
    input_dir = os.path.dirname(file_path)
    output_file_path = os.path.join(input_dir, 'cwnd.png')
    plt.savefig(output_file_path)

    plt.close()

def plot_multiple_cwnd(dir_path):
    # extract domain name in dir_path
    domain_name = dir_path.split('/')[-1]
    
    # plot line chart using /dir_path/windows.csv
    # plot dot using /dir_path/window*.csv
    base_path = dir_path + '/windows.csv'
    df = pd.read_csv(base_path, header=None, sep=' ', names=['a', 'cwnd', 'RTT'])
    # 提取第二列的值作为cwnd，第三列的值作为时间
    cwnd_values = df['cwnd']
    time_values = df['RTT']
    # 绘制cwnd随时间变化的图
    plt.figure(figsize=(10, 5))
    plt.plot(time_values, cwnd_values)  # 使用圆点标记每个数据点
    plt.title(f'{domain_name}')
    plt.xlabel('RTT')
    plt.ylabel('CWND')
    
    idx = np.arange(len(time_values))
    for i in range(5):
        cur_file_path = f"{dir_path}/windows{i+1}.csv"
        df = pd.read_csv(cur_file_path, header=None, sep=' ', names=['a', 'cwnd', 'RTT'])
        cwnd_values = df['cwnd']
        # with different colors
        plt.scatter(idx, cwnd_values, label=f'trial {i+1}')
        # plt.scatter(idx, cwnd_values, color='red', label=f'Window {i}')

    plt.grid(True)
    plt.legend()
    # plt.show()
    plt.savefig(f"{dir_path}/{domain_name}_cwnd.png")
    plt.savefig(f"../figures/{domain_name}_cwnd.png")
    


def test():
    # 假设x和y是两个长度相同的列表
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]

    # 绘制x的折线图
    plt.plot(x, label='Line for x')

    # 在x的每个位置上绘制y的点
    idx = np.arange(len(x))
    plt.scatter(idx, y, color='red', label='Points for y')

    # 添加图例
    plt.legend()

    # 设置图表标题和轴标签
    plt.title('Line and Points Plot')
    plt.xlabel('X values')
    plt.ylabel('Y values')

    # 显示图表
    plt.show()


def draw_size_distri(sizePath, plotPath):
    data = []
    sizeFile = open(sizePath)
    csvReader = csv.reader(sizeFile)
    sizeInfos = list(csvReader)
    sizeFile.close()
    
    for i in range(len(sizeInfos)):
        # print(urlInfos[i])
        sizeInfos[i] = sizeInfos[i][0].split(" ")
        web_size = str(sizeInfos[i][1])
        data.append(int(web_size) / 1000) # /KB
    
    # compute cdf
    sorted_data = sorted(data)
    sorted_data = [x for x in sorted_data if x > 0]
    # print top five biggest and smallest web page sizes (> 0)
    print(sorted_data[-5:])
    print(sorted_data[:5])
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    # plot cdf
    plt.step(sorted_data, cdf, where='post', label='CDF')
    plt.xscale('log')
    plt.title('CDF of web page sizes')
    plt.xlabel('web page size(KB)')
    plt.ylabel('CDF')
    plt.legend()
    # plt.savefig(plotPath)
    
    
if __name__ == '__main__':
    # plot_cwnd(file_path)
    # test()
    # plot_multiple_cwnd(file_path)
    draw_size_distri("../Alexa20k/web_size.csv",
                     "../figures/size_distri.png")
    
