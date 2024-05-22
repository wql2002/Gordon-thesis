import pandas as pd
import os

# 设置工作目录到包含CSV文件的文件夹
# 假设所有文件都在当前目录下
directory = '.'

# 获取所有以windows${i}.csv命名的文件
files = [f for f in os.listdir(directory) if f.startswith('windows') and f.endswith('.csv')]

# 初始化一个空的DataFrame来存储第二列的数据
data = pd.DataFrame()

# 遍历所有文件
for file in files:
    # 读取CSV文件
    df = pd.read_csv(os.path.join(directory, file), header=None, names=['col1', 'col2', 'col3'])
    # 添加第二列数据到data DataFrame中
    data[file] = df['col2']

# 计算每个时刻的最大值
max_values = data.max(axis=1)

# 将最大值序列写入到新的CSV文件中
max_values.to_csv('windows.csv', header=False, index=False)