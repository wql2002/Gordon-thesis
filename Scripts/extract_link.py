import csv

# 输入文件名
input_filename = '../Alexa20k/exp_links.csv'
# 输出文件名
output_filename = '../Alexa20k/cwnd_result.csv'

# 用于存储提取的域名
domains = []

# 打开输入文件并读取第二列
with open(input_filename, mode='r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        row = row[0].split(" ")
        if len(row) > 1:  # 确保行中有足够的列
            domain = row[1]  # 提取第二列
            domains.append(domain)

# print(domains)
# 将提取的域名写入输出文件
with open(output_filename, mode='a', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for domain in domains:
        csvwriter.writerow([domain])  # 写入单个元素的行

print(f'Domains have been extracted and written to {output_filename}')