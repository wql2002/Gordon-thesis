import sys
import os
import csv

if __name__ == "__main__":
    # arg0 = sys.argv[0]
    # arg1 = sys.argv[1]
    
    # print(arg0)
    # print(arg1)
    projHomePath = "/home/ubuntu/Gordon"
    # projHomePath = "/home/vagrant"

    urlFilePath = projHomePath + "/Data/google.com/windows1.csv"
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