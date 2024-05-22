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
parser.add_argument('-e', type = int, default = 10,
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
    # if urlInfos[i][1] not in analysisResult.read().splitlines():
        # if urlInfos[i][3] == '':
        # if 1:
        #print(urlInfos[i][1])
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
            # subprocess.call(["./clean.sh"], shell=True, executable="/bin/bash")
            # subprocess.call(["cp ../Data/windows.csv ../Windows/"+urlInfos[i][1]+".csv"], shell=True, executable="/bin/bash")
            #subprocess.call(["exit"], shell=True, executable="/bin/bash")
        
        print("over")
        # cwnd_path = projHomePath + "/Data/" + targetDomain + "/windows.csv"
        # read_mode = 0
        # # 
        # cc_type = tcpClassify.classify(cwnd_path, read_mode)
        # csvOutputFile = open(outputFile, 'a')
        # csvWriter = csv.writer(csvOutputFile)
        # csvWriter.writerow([targetDomain, cc_type, targetURL])
        # csvOutputFile.close()
        i += 1
        time.sleep(10)

        # else:
        #     """
        #     while True:
        #         print(urlInfos[i][1], urlInfos[i][2:])
        #         try:
        #             request = Request(urlInfos[i][2])
        #             request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0')
        #             html = urlopen(request)
        #         except HTTPError as e:
        #             if e.code == 404:
        #                 print(e)
        #                 i += 1
        #         except Exception as e:
        #             print(e)
        #             i += 1
        #         else:
        #             break
        #     """
        
        #     j = i

        #     try:
        #         response = subprocess.check_output(
        #             ['ping', '-c', '1', urlInfos[i][1]],
        #             stderr=subprocess.STDOUT,  # get all output
        #             universal_newlines=True  # return string not bytes
        #         )
        #     except subprocess.CalledProcessError:
        #         response = None

        #     if response == None:
        #         pingTime = -1
        #     else:
        #         pingTime = float(re.search('time=.*', response).group().replace(" ms", '')[5:])

        #     if int(pingTime/2) >= 50:
        #         delayTime = 1
        #     elif pingTime == -1:
        #         delayTime = 50
        #     else:
        #         delayTime = 50 - int(pingTime/2)

        #     print(urlInfos[i][3], delayTime)

        #     try:
        #         subprocess.call(["mm-delay " + str(delayTime) + " ./multi-launch.sh '"+urlInfos[i][2]+"' 10"], shell=True, executable='/bin/bash')
        #         #subprocess.call(["./multi-launch.sh "+urlInfos[j][2]+" 10"], shell=True, executable='/bin/bash')
        #     except Exception as e:
        #         print(e)
        #     finally:
        #         subprocess.call(["./clean.sh"], shell=True, executable="/bin/bash")
        #         subprocess.call(["cp ../Data/windows.csv ../Windows/"+urlInfos[i][0]+"-"+urlInfos[i][1]+".csv"], shell=True, executable="/bin/bash")
        #         #subprocess.call(["exit"], shell=True, executable="/bin/bash")
            
        #     type = tcpClassify.classify()
        #     #type = "undecided"
        #     csvOutputFile = open("./analysisResult.csv", 'a')
        #     csvWriter = csv.writer(csvOutputFile)
        #     csvWriter.writerow([urlInfos[i][1], type, urlInfos[j][3]])
        #     csvOutputFile.close()
        #     csvOutputFile = open("./domainResult.csv", 'a')
        #     csvWriter = csv.writer(csvOutputFile)
        #     csvWriter.writerow([urlInfos[i][1]])
        #     csvOutputFile.close()
        #     while urlInfos[j][1] == urlInfos[i][1]:
        #         j+=1
        #     i = j
        #     time.sleep(10)
        #     #input()
            
        #     """
        #     while urlInfos[j][0] == urlInfos[i][1]:
        #         try:
        #             subprocess.call(["./multi-launch.sh "+urlInfos[j][2]], shell=True, executable='/bin/bash')
        #         except Exception as e:
        #             print(e)
        #         finally:
        #             subprocess.call(["./clean.sh"], shell=True, executable="/bin/bash")
                
        #         type = tcpClassify.classify()
        #         csvOutputFile = open("./analysisResult.csv", 'a')
        #         csvWriter = csv.writer(csvOutputFile)
        #         csvWriter.writerow([urlInfos[i][1], type, urlInfos[j][2]])
        #         csvOutputFile.close()
        #         csvOutputFile = open("./domainResult.csv", 'a')
        #         csvWriter = csv.writer(csvOutputFile)
        #         csvWriter.writerow([urlInfos[i][1]])
        #         csvOutputFile.close()
        #         input()
        #         j += 1
        #     #targetURL = urlInfos[i][2]
        #     i = j
        #     """

    else:
        print("Already Done, Next...")
        i += 1
    
    
    
    #input()

