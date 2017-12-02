#!/bin/bash

sudo systemctl enable ssh
sudo usermod -p $(echo $1 | openssl passwd -1 -stdin) pi

