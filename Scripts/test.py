import sys
import os
import csv
import subprocess
import tcpClassify
import matplotlib.pyplot as plt
import numpy as np

def data_proc1(urlFilePath):
    # projHomePath = ".."
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
    # open file
    urlFile = open(urlFilePath)
    csvReader = csv.reader(urlFile)
    urlInfos = list(csvReader)
    urlFile.close()
    # count results by cc types
    for i in range(start, end):
        # print(urlInfos[i])
        urlInfos[i] = urlInfos[i][0].split(" ")
        domain_name = urlInfos[i][0]
        result = urlInfos[i][1]
        
        if result in result_counts:
            result_counts[result] += 1
        else:
            result_counts[result] = 1
    
    # show result
    total = sum(result_counts.values())
    sorted_results = sorted(result_counts.items(), key=lambda item: item[1], reverse=True)
    
    for result, count in sorted_results:
        print(f"{result}: {count / total:.2%}")


def test_wget(urlFilePath, end, start = 0):
    # open and read .csv file 
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

def get_size_distri(urlFilePath, resultPath, sizePath, end, start = 0):
    # open and read .csv file 
    urlFile = open(urlFilePath)
    csvReader = csv.reader(urlFile)
    urlInfos = list(csvReader)
    urlFile.close()
    
    resultFile = open(resultPath)
    csvReader = csv.reader(resultFile)
    resultInfos = list(csvReader)
    resultFile.close()
    
    for i in range(start, end):
        # print(urlInfos[i])
        urlInfos[i] = urlInfos[i][0].split(" ")
        url_domain = str(urlInfos[i][1])
        url_link = str(urlInfos[i][2])
        
        resultInfos[i] = resultInfos[i][0].split(" ")
        url_result = str(resultInfos[i][1])
        
        # print(f"url_result: {url_result}")
        if (url_result == "[FAIL]" or 
            url_result == "[TODO]" or 
            url_result == "[FORBID]" or 
            url_result == "[SHORT]"):
            with open(sizePath, 'a') as f:
                f.write(f"{url_domain} {0}\n")
            continue
        
        try:
            cmd = ["wget", "-U", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0',
                   "-O", "indexPage", "--no-check-certificate", url_link]
            subprocess.run(cmd)
            # subprocess.call(["mm-delay " + str(delayTime) + " ./multi-launch.sh " + targetURL + " 5 " + targetDomain], shell=True, executable='/bin/bash')
            #subprocess.call(["./multi-launch.sh "+targetURL+" 10"], shell=True, executable='/bin/bash')
        except Exception as e:
            print(e)
        
        file_size = os.path.getsize("indexPage")
        if file_size <= 100000:
            try:
                cmd = ["rm", "indexPage"]
                subprocess.run(cmd)
                cmd = ["wget", "-U", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0',
                    "-O", "indexPage", "--no-check-certificate", url_domain]
                subprocess.run(cmd)
            except Exception as e:
                print(e)

        file_size = os.path.getsize("indexPage")
        with open(sizePath, 'a') as f:
            f.write(f"{url_domain} {file_size}\n")
        cmd = ["rm", "indexPage"]
        subprocess.run(cmd)


    

if __name__ == "__main__":
    # data_proc1("../Data/google.com/windows1.csv")
    count_results("../Alexa20k/cwnd_result.csv", 200)
    # test_wget("../Alexa20k/exp_links.csv", 133, 124)
    # cc_clasify("../Alexa20k/cwnd_result.csv", 211, 198)
    # get_size_distri("../Alexa20k/exp_links.csv",
    #                 "../Alexa20k/cwnd_result.csv",
    #                 "../Alexa20k/web_size.csv",
    #                 end = 200, start = 116)
    
    