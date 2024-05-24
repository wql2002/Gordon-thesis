# Usage: python3 plot.py <path/to/file>

import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('path', type = str,
                    help = "A required string to specify the file path")
args = parser.parse_args()

file_path = args.path

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