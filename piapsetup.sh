#!/bin/bash
SIP=${PI_IP_NET:-192.168.11}

sudo killall -9 /sbin/dhcpcd
sudo killall -9 dnsmasq

sudo ifconfig wlan0 up ${SIP}.1 netmask 255.255.255.0
sleep 5

cat dnsmasq.conf.template | sed "s//SIP/g" > /tmp/dnsmasq.conf
sudo dnsmasq -C /tmp/dnsmasq.conf

AP="pi_`ip add show wlan0 |awk '/ether/{print $2}'|sed 's/://g'`"
PASS=`tr -cd '[:alnum:]' < /dev/urandom | fold -w8 | head -n1`

cat hostapd.conf.template | sed "s/NETNAME/${AP}/g;s/NETPASS/${PASS}/g" > /tmp/hostapd.conf
DISPLAY=:0 zenity --warning --no-wrap --text="Wifi password for $AP set to : $PASS\nConnect to http://${SIP}.1:5678 to setup your Pi" &

sudo hostapd /tmp/hostapd.conf