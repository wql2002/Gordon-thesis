import csv
import tcpClassify

input_filename = '../Alexa20k/cwnd_result.csv'
domains = []

with open(input_filename, mode='r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    line = 0
    for row in csvreader:
        row = row[0].split(" ")
        # print(row)
        if len(row) == 1:  # 确保行中有足够的列
            cwnd_path = "../Data/" + str(row[0]) + "/windows.csv"
            try:
                cc_result = tcpClassify.classify(cwnd_path, 0)
                print(f"[{row[0]}]: {cc_result}")
            except Exception as e:
                print(f"Exception: {e}")
        line += 1
        if line == 117:
            break

print("Finish...")