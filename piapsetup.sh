#!/bin/bash

sudo ifconfig wlan0 up 192.168.191.1 netmask 255.255.255.0
sleep 5
sudo dnsmasq -C ./dnsmasq.conf

AP="pi_`ip add show wlan0 |awk '/ether/{print $2}'|sed 's/://g'`"
PASS=`tr -cd '[:alnum:]' < /dev/urandom | fold -w10 | head -n1`
PASS="b123456789"

cat hostapd.conf | sed "s/NETNAME/${AP}/g;s/NETPASS/${PASS}/g" > /tmp/hostapd.conf
DISPLAY=:0 zenity --warning --no-wrap --text="Wifi password for $AP set to : $PASS\nConnect to http://192.168.1.191.1:5678 to setup your Pi" &

sudo killall -9 /sbin/dhcpcd

sudo hostapd /tmp/hostapd.conf