#Usage: ./launch_cont.sh <target URL> <Index number - for repeated tests>

SRC_PATH="/home/vagrant"
# NETIF_NAME="ech0" # default interface name
NETIF_NAME="ingress"
# DST_ADDR="192.168.121.67"
DST_ADDR="100.64.0.2"
URL=${1:-"www.baidu.com"}
START=${2:-"1"}

echo "[Gordon] start testing!"
echo "[Gordon] set up network interface MTU"
sudo ifconfig ${NETIF_NAME} mtu 296
echo "[Gordon] complie probe.c into executable..."
gcc -Wall -o ${SRC_PATH}/src/prober ${SRC_PATH}/src/probe.c -lnfnetlink -lnetfilter_queue -lpthread -lm

for ((i = ${START}; i <= 100; i++));
do

	sudo iptables -I INPUT -p tcp -d ${DST_ADDR} -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
	echo "--------------------------------- RTT-$i ----------------------"
	sudo ${SRC_PATH}/src/prober ${URL} 8000 5000 1000
	# sudo ${SRC_PATH}/src/prober ${URL} 8000 5000 1000 >> ${SRC_PATH}/Data/buff.csv
	sleep 20
	rm -f index*
	sudo iptables --flush
	echo ""
	echo "[RTT-$i] finish..."
	sleep 30
done

