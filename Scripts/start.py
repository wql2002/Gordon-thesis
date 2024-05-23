# usage: python3 start.py <pos of links> [-s: start trial number] [-e: end trial number]

import csv
import subprocess
import argparse
# import tcpClassify
# from urllib.request import Request
# from urllib.request import urlopen
# from urllib.error import HTTPError
import time
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('start', type = int,
                    help = "A required integer to specify the start position of url links")
parser.add_argument('--switch', action='store_true',
                    help = "An optional switch to specify the open file")
parser.add_argument('-s', type = int, default = 1,
                    help = "The start point of trial number")
parser.add_argument('-e', type = int, default = 5,
                    help = "The end point of trial number")
args = parser.parse_args()

projHomePath = "/home/ubuntu/Gordon"
# projHomePath = "/home/vagrant"

if not args.switch:
    urlFilePath = projHomePath + "/Alexa20k/exp_links.csv"
else:
    urlFilePath = projHomePath + "/Alexa20k/full_links.csv"
print(urlFilePath)
urlFile = open(urlFilePath)
csvReader = csv.reader(urlFile)
urlInfos = list(csvReader)
#print(urlInfos)
urlFile.close()

outputFile = projHomePath + "/Alexa20k/cwnd_result.csv"

#measure 150 websites from the strat point.
# start = int(sys.argv[1])
start = args.start
i = start

while i < start + len(urlInfos):
    cur_url_status = None
    urlInfos[i] = urlInfos[i][0].split(" ")
    # print(urlInfos[i])
    try:
        cur_url_status = urlInfos[i][3]
    except Exception as e:
        # print(e)
        cur_url_status = "notdone"
    
    if cur_url_status == "notdone":
        targetIndex = urlInfos[i][0]
        targetDomain = urlInfos[i][1]
        targetURL = urlInfos[i][2]
        print('\n\n\n\n[start.py][OFFSET-{}] {}'.format(i, targetIndex))
        print('                      {}'.format(targetDomain))
        print('                      {}'.format(targetURL))
        # print("===================================================>", targetURL, "\n================", targetIndex, targetDomain, targetURL)

        try:
            response = subprocess.check_output(
                ['ping', '-c', '1', targetDomain],
                stderr=subprocess.STDOUT,  # get all output
                universal_newlines=True  # return string not bytes
            )
        except subprocess.CalledProcessError:
            response = None

        if response == None:
            pingTime = -1
        else:
            pingTime = float(re.search('time=.*', response).group().replace(" ms", '')[5:])

        if int(pingTime/2) >= 50:
            delayTime = 1
        elif pingTime == -1:
            delayTime = 50
        else:
            delayTime = 50 - int(pingTime/2)

        print(targetURL, delayTime)
        
        try:
            cmd = ["mm-delay", str(delayTime), "/bin/bash", "./multi-launch.sh", targetURL, str(args.s), str(args.e), targetDomain]
            subprocess.run(cmd)
            # subprocess.call(["mm-delay " + str(delayTime) + " ./multi-launch.sh " + targetURL + " 5 " + targetDomain], shell=True, executable='/bin/bash')
            #subprocess.call(["./multi-launch.sh "+targetURL+" 10"], shell=True, executable='/bin/bash')
        except Exception as e:
            print(e)
        finally:
            cmd = ["/bin/bash", "./clean.sh"]
            subprocess.run(cmd)

        print("over")
        i += 1
        time.sleep(10)

    else:
        print("Already Done, Next...")
        i += 1
    
    
    
    #input()

