import sys
import os
import csv
import subprocess
import tcpClassify

def data_proc1(urlFilePath):
    # projHomePath = "/home/ubuntu/Gordon"
    # # projHomePath = "/home/vagrant"

    # urlFilePath = projHomePath + "/Data/google.com/windows1.csv"
    print(urlFilePath)
    urlFile = open(urlFilePath)
    csvReader = csv.reader(urlFile)
    urlInfos = list(csvReader)
    urlFile.close()
    
    for i in range(1, len(urlInfos)):
        # print(urlInfos[i])
        urlInfos[i] = urlInfos[i][0].split(" ")
        urlInfos[i][2] = int(urlInfos[i][2])
        urlInfos[i][2] -= 3
        # urlInfos[i] = urlInfos[i].join(" ")
    
    with open(urlFilePath, 'w', newline='') as urlFile:
        csvWriter = csv.writer(urlFile, delimiter=' ')
        csvWriter.writerows(urlInfos)

def count_results(urlFilePath, end, start = 0):
    result_counts = {}
    
    urlFile = open(urlFilePath)
    csvReader = csv.reader(urlFile)
    urlInfos = list(csvReader)
    urlFile.close()
    
    for i in range(start, end):
        # print(urlInfos[i])
        urlInfos[i] = urlInfos[i][0].split(" ")
        domain_name = urlInfos[i][0]
        result = urlInfos[i][1]
        
        if result in result_counts:
            result_counts[result] += 1
        else:
            result_counts[result] = 1
    
    total = sum(result_counts.values())
    for result, count in result_counts.items():
        print(f"{result}: {count / total:.2%}")


def test_wget(urlFilePath, end, start = 0):
    urlFile = open(urlFilePath)
    csvReader = csv.reader(urlFile)
    urlInfos = list(csvReader)
    urlFile.close()
    
    for i in range(start, end):
        # print(urlInfos[i])
        urlInfos[i] = urlInfos[i][0].split(" ")
        url_link = str(urlInfos[i][2])
        
        try:
            cmd = ["wget", "-U", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0',
                   "-O", "indexPage", "--no-check-certificate", url_link]
            subprocess.run(cmd)
            # subprocess.call(["mm-delay " + str(delayTime) + " ./multi-launch.sh " + targetURL + " 5 " + targetDomain], shell=True, executable='/bin/bash')
            #subprocess.call(["./multi-launch.sh "+targetURL+" 10"], shell=True, executable='/bin/bash')
        except Exception as e:
            print(e)
        finally:
            cmd = ["rm", "index*", "wget-log*"]
            subprocess.run(cmd)

def cc_clasify(urlFilePath, end, start = 0):
    urlFile = open(urlFilePath)
    csvReader = csv.reader(urlFile)
    urlInfos = list(csvReader)
    urlFile.close()
    
    for i in range(start, end):
        # print(urlInfos[i])
        urlInfos[i] = urlInfos[i][0].split(" ")
        domain_name = str(urlInfos[i][0])
        
        if len(urlInfos[i]) == 1:
            cwnd_path = "../Data/" + domain_name + "/windows.csv"
            try:
                cc_result = tcpClassify.classify(cwnd_path, 0)
                print(f"[{domain_name}]:\t\t{cc_result}")
            except Exception as e:
                print(f"Exception: {e}")


if __name__ == "__main__":
    # arg0 = sys.argv[0]
    # arg1 = sys.argv[1]
    
    # print(arg0)
    # print(arg1)
    # data_proc1("/home/ubuntu/Gordon/Data/google.com/windows1.csv")
    # count_results("/home/ubuntu/Gordon/Alexa20k/cwnd_result.csv", 121)
    # test_wget("/home/ubuntu/Gordon/Alexa20k/exp_links.csv", 133, 124)
    cc_clasify("/home/ubuntu/Gordon/Alexa20k/cwnd_result.csv", 138, 131)