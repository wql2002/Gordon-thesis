#Usage: ./multi-launch.sh <target URL> <Index number - for repeated tests> <target domain name>

SRC_PATH="/home/ubuntu/Gordon"
# SRC_PATH="/home/vagrant"
NETIF_NAME="ingress" # default interface name
# DST_ADDR="192.168.121.67"
DST_ADDR="100.64.0.2"
URL=${1:-"www.baidu.com"}
START=${2:-1}		# starting point of trials
END=${3:-5}		# ending point of trials
DOMAIN_NAME=${4:-"baidu.com"}
URL_CASE=0
SKIP_FLAG=0

echo "[DEBUG]: " ${URL} ${END} ${DOMAIN_NAME}
# ip address show

sudo sysctl net.ipv4.tcp_sack=0
sudo ifconfig ${NETIF_NAME} mtu 120
gcc -o ${SRC_PATH}/src/multi-prober ${SRC_PATH}/src/multi-probe.c -lnfnetlink -lnetfilter_queue -lpthread -lm

# create directory if not existed
if [ ! -d "${SRC_PATH}/Data/${DOMAIN_NAME}" ]; then
	echo "[TEST] create dir: ${SRC_PATH}/Data/${DOMAIN_NAME}"
    mkdir -p "${SRC_PATH}/Data/${DOMAIN_NAME}"
	# fill in with initial data
	for (( c=$START; c<=$END; c++ ))
	do
		echo "0 0 0" > ${SRC_PATH}/Data/${DOMAIN_NAME}/windows$c.csv
	done

	echo "0 0 0" > ${SRC_PATH}/Data/${DOMAIN_NAME}/windows.csv
	echo "0 0" > ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv
fi

check_wget_finish() {
	local file_path="$1"
	local sleep_time="${2:-2}"  # poll time (default 2s)
	local search_string1="WGET DONE"
	local search_string2="WGET END"
	local search_string3="EXP FINISH"
	local search_string4="SKIP"

	if grep ${search_string4} ${file_path}; then
		SKIP_FLAG=1
	else
		SKIP_FLAG=0
	fi
}

clean_up() {
	rm -f index* wget-log*
}

check_web_size() {
	local url=$1
    local user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'

    # download the page
    wget -t 10 -T 45 -U "$user_agent" -O indexPage --no-check-certificate "$url"

    # check if wget succeeded
    if [ $? -ne 0 ]; then
        # download failed
		clean_up
        URL_CASE=2
    fi

    # check downloaded page's size
    if [ $(du -k indexPage | cut -f1) -lt 100 ]; then
		# size <= 100k
		clean_up
        URL_CASE=1
    else
		# size > 100k
		clean_up
        URL_CASE=0
    fi

}

set_url() {
	local case=${1:-0}

	case ${case} in
		0)
			echo "[MULTI-LAUNCH] use origin URL ${URL}"
			;;
		1|2)
			URL=${DOMAIN_NAME}
			echo "[MULTI-LAUNCH] change URL to ${URL}"
			;;
	esac
}

# ------------------------------ RUN EXPERIMENT ------------------------------
# determine wget target url
check_web_size ${URL}
set_url ${URL_CASE}

# determine RTT range
RTT_START=$(wc -l < ${SRC_PATH}/Data/${DOMAIN_NAME}/windows.csv)
RTT_END=50

# begin exp
for ((i = ${RTT_START}; i <= ${RTT_END}; i++));
do
	for (( j=$START; j<=$END; j++ ))
	do
		sleep 2
		sudo iptables -I INPUT -p tcp -d ${DST_ADDR} -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
		echo "--------------------------------- RTT-$i, TRIAL-$j ----------------------"
		sudo ${SRC_PATH}/src/multi-prober ${URL} 2000 3000 1500 "$j" ${DOMAIN_NAME} >> ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv
		# sleep 2000
		# sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME} > ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv &
		# check_wget_finish ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv
		# sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME} > ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv
		# sudo killall wget multi-prober
		rm -f index* wget-log*	# remove extra files
		sudo iptables --flush
	done

	# check if wget finish, if yes, exit
	# echo "[SKIP_FLAG] = ${SKIP_FLAG}"
	check_wget_finish ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv
	cp ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv ${SRC_PATH}/Data/${DOMAIN_NAME}/buff-bak.csv # back up
	echo "" > ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv # clear buff.csv content
	# echo "[SKIP_FLAG] = ${SKIP_FLAG}"
	if [ ${SKIP_FLAG} = 1 ]; then
		echo "[multi-lauch.sh] early exit..."
		exit 0
	fi

	python3 getmedian.py $i $END ${DOMAIN_NAME} ${SRC_PATH}

	if [ `tail -n 1 ${SRC_PATH}/Data/${DOMAIN_NAME}/windows.csv | cut -d" " -f2` == "0" ]; then
		exit 0
	fi
done

# i: RTT, j: trial number

# for (( j=$START; j<=$END; j++ ))
# 	do
# 	RTT_START=$(wc -l < ${SRC_PATH}/Data/${DOMAIN_NAME}/windows${j}.csv)
# 	RTT_END=50
# 	for ((i = ${RTT_START}; i <= ${RTT_END}; i++));
# 		do
# 		sleep 3
# 		sudo iptables -I INPUT -p tcp -d ${DST_ADDR} -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
# 		echo "--------------------------------- RTT-$i, TRIAL-$j ----------------------"
# 		sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME}
# 		# sleep 2000
# 		# sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME} > ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv &
# 		# check_wget_finish ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv
# 		# sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME} > ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv
# 		# sudo killall wget multi-prober multi-launch
# 		rm -f index* wget-log*	# remove extra files
# 		sudo iptables --flush
# 	done

# 	# python3 getmedian.py $i $END ${DOMAIN_NAME} ${SRC_PATH}
	
# 	if [ `tail -n 1 ${SRC_PATH}/Data/${DOMAIN_NAME}/windows.csv | cut -d" " -f2` == "0" ]; then
# 		exit 0
# 	fi
# done

rm -f index*
