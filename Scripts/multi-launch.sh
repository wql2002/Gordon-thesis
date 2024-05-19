#Usage: ./multi-launch.sh <target URL> <Index number - for repeated tests> <target domain name>

SRC_PATH="/home/vagrant"
NETIF_NAME="ingress" # default interface name
# DST_ADDR="192.168.121.67"
DST_ADDR="100.64.0.2"
URL=${1:-"www.baidu.com"}
START=1		# starting point of trials
END=${2:-10}		# ending point of trials
DOMAIN_NAME=${3:-"baidu.com"}

echo "[DEBUG]: " ${URL} ${END} ${DOMAIN_NAME}

sudo sysctl net.ipv4.tcp_sack=0
sudo ifconfig ${NETIF_NAME} mtu 100
gcc -Wall -o ${SRC_PATH}/src/multi-prober ${SRC_PATH}/src/multi-probe.c -lnfnetlink -lnetfilter_queue -lpthread -lm

# create directory if not existed
if [ ! -d "${SRC_PATH}/Data/${DOMAIN_NAME}" ]; then
	echo "[TEST] create dir: ${SRC_PATH}/Data/${DOMAIN_NAME}"
    mkdir -p "${SRC_PATH}/Data/${DOMAIN_NAME}"
fi

for (( c=$START; c<=$END; c++ ))
do
echo "0 0 0" > ${SRC_PATH}/Data/${DOMAIN_NAME}/windows$c.csv
done

echo "0 0 0" > ${SRC_PATH}/Data/${DOMAIN_NAME}/windows.csv
echo "0 0" > ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv

for i in {1..50}
do
#sudo iptables -I INPUT -p tcp -d 100.64.0.2 -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
#python getmedian.py $i	
	for (( j=$START; j<=$END; j++ ))
	do
		sudo iptables -I INPUT -p tcp -d ${DST_ADDR} -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
		echo "--------------------------------- RTT-$i, TRIAL-$j ----------------------"
		sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME}
		# sudo ${SRC_PATH}/src/multi-prober "$1" 2000 3000 1500 "$j" ${DOMAIN_NAME} >> ${SRC_PATH}/Data/${DOMAIN_NAME}/buff.csv
		sudo killall wget
		rm -f index*
		sudo iptables --flush
	done
python getmedian.py $i $END ${DOMAIN_NAME}
if [ `tail -n 1 ${SRC_PATH}/Data/${DOMAIN_NAME}/windows.csv | cut -d" " -f2` == "0" ]; then
	exit 0
fi
#sudo iptables --flush
done

rm -f index*
#mkdir ../Data/fb-$2
#mv ../Data/windows* ../Data/fb-$2/

#mv windows.csv "testResults/windows-$1-$2.csv"
#sudo iptables --flush
