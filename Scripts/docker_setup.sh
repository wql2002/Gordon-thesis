#!/bin/bash

docker run -it --cap-add=NET_ADMIN --cap-add=NET_RAW --device=/dev/net/tun --privileged ubuntu:16.04 /bin/bash