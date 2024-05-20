sudo apt-get update && sudo aapt-getpt upgrade -y
sudo apt-get install -y python
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
python3 -m pip install numpy
#sudo python3-pip install numpy
# sudo add-apt-repository ppa:keithw/mahimahi -y
# sudo apt-get update
# sudo apt-get install -y mahimahi
sudo apt-get install -y protobuf-compiler libprotobuf-dev \
    autotools-dev dh-autoreconf iptables pkg-config dnsmasq-base \
    apache2-bin apache2-dev debhelper libssl-dev ssl-cert \
    libxcb-present-dev libcairo2-dev libpango1.0-dev
cd ~
git clone https://github.com/ravinet/mahimahi
cd mahimahi
./autogen.sh
./configure
make
sudo make install
sudo dpkg-reconfigure -p critical dash
sudo sysctl -w net.ipv4.ip_forward=1
sudo apt-get install -y libnetfilter-queue-dev
sudo apt-get install tmux

# apt-get install sudo -y   # for Docker
sudo apt-get install -y iputils-ping
sudo apt-get install -y wget
sudo apt-get install -y psmisc
sudo apt install -y net-tools

#relocating iptables in some instances of Ubuntu
sudo cp /etc/alternatives/iptables /sbin/iptables
