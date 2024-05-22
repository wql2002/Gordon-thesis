#Usage: ./multi-launch.sh <target URL> <Index number - for repeated tests> <target domain name>

SRC_PATH="/home/ubuntu/Gordon"
# SRC_PATH="/home/vagrant"
NETIF_NAME="ingress" # default interface name
# DST_ADDR="192.168.121.67"
DST_ADDR="100.64.0.2"
URL=${1:-"www.baidu.com"}
START=${2:-1}		# starting point of trials
END=${3:-10}		# ending point of trials
DOMAIN_NAME=${4:-"baidu.com"}

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
	local search_string1="[WGET DONE]"
	local search_string2="[WGET END]"
	local search_string3="[EXP FINISH]"

	# poll until wget finish
	while true; do
		if grep "${search_string1}" "${file_path}"; then
			echo "[CASE 0] finish RTT-${i} ${j}-th trial" 
			sudo killall multi-prober
			return 0
		# elif grep "${search_string2}" "${file_path}"; then
		# 	# wait for proc writing data
		# 	while true; do
		# 		sleep 1
		# 		if grep "${search_string3}" "${file_path}"; then
		# 			break
		# 		fi
		# 	done
		# 	echo "[CASE 1] finish RTT-${i} ${j}-th trial" 
		# 	# sudo killall wget multi-prober
		# 	return 0
		elif grep "${search_string3}" "${file_path}"; then
			echo "[CASE 1] finish RTT-${i} ${j}-th trial" 
			return 0
		else
			sleep "${sleep_time}"  # sleep to wait for another try
		fi
	done
}

# ------------------------------ RUN EXPERIMENT ------------------------------

# RTT_START=$(wc -l < ${SRC_PATH}/Data/${DOMAIN_NAME}/windows.csv)
# RTT_END=35

# for ((i = ${RTT_START}; i <= ${RTT_END}; i++));
# do
# 	for (( j=$START; j<=$END; j++ ))
# 	do
# 		sleep 2
# 		sudo iptables -I INPUT -p tcp -d ${DST_ADDR} -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
# 		echo "--------------------------------- RTT-$i, TRIAL-$j ----------------------"
# 		# sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME}
# 		# sleep 2000
# 		# sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME} > ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv &
# 		# check_wget_finish ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv
# 		sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME} > ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv
# 		# sudo killall wget multi-prober multi-launch
# 		rm -f index* wget-log*	# remove extra files
# 		sudo iptables --flush
# 	done

# 	python3 getmedian.py $i $END ${DOMAIN_NAME} ${SRC_PATH}

# 	if [ `tail -n 1 ${SRC_PATH}/Data/${DOMAIN_NAME}/windows.csv | cut -d" " -f2` == "0" ]; then
# 		exit 0
# 	fi
# done

# i: RTT, j: trial number

for (( j=$START; j<=$END; j++ ))
	do
	RTT_START=$(wc -l < ${SRC_PATH}/Data/${DOMAIN_NAME}/windows${j}.csv)
	RTT_END=50
	for ((i = ${RTT_START}; i <= ${RTT_END}; i++));
		do
		sleep 3
		sudo iptables -I INPUT -p tcp -d ${DST_ADDR} -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
		echo "--------------------------------- RTT-$i, TRIAL-$j ----------------------"
		sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME}
		# sleep 2000
		# sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME} > ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv &
		# check_wget_finish ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv
		# sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME} > ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv
		# sudo killall wget multi-prober multi-launch
		rm -f index* wget-log*	# remove extra files
		sudo iptables --flush
	done

	# python3 getmedian.py $i $END ${DOMAIN_NAME} ${SRC_PATH}
	
	if [ `tail -n 1 ${SRC_PATH}/Data/${DOMAIN_NAME}/windows.csv | cut -d" " -f2` == "0" ]; then
		exit 0
	fi
done

rm -f index*
