sudo pkill -f start.py
sudo killall mm-delay wget multi-prober multi-launch.sh 
rm -f index* wget-log*
sudo iptables --flush
