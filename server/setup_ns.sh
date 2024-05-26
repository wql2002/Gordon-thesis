# create ns
sudo ip netns add ns1
# add veth peer
sudo ip link add ns1-veth type veth peer name ns1-br-veth
# bind veth to ns
sudo ip link set ns1-veth netns ns1
# add ip addr to veth
sudo ip netns exec ns1 ip addr add 10.10.0.10/16 dev ns1-veth
# create bridge and bind veth peer
sudo ip link add br0 type bridge
sudo ip link set ns1-br-veth master br0
# set up link
sudo ip link set br0 up
sudo ip link set ns1-br-veth up
# set up ns1 dev
sudo ip netns exec ns1 ip link set dev lo up
sudo ip netns exec ns1 ip link set dev ns1-veth up
# set ip addr to bridge
sudo ip addr add 10.10.0.1/16 dev br0
sudo ip netns exec ns1 ip route add default via 10.10.0.1

